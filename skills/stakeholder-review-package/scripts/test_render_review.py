"""Behavioral checks with a fictional project, independent of private pilot files."""
import copy
import base64
import json
import tempfile
import subprocess
import sys
import unittest
from pathlib import Path
from render_review import EmbeddedImages, digest, manifest, render, validate, load_authoring, authoring_digest, embedded_json


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'class-bookings-prd.md').write_text('# Community classes\nAC-BOOK-01: Show availability.\n')
        (self.root / 'class-bookings-assumptions.md').write_text('# Assumptions\n### RULE-001. Cancellation\nA cancellation frees a place.\n### UI-001. Waiting list\nShow the queue position.\n## Validated Assumptions\n### RULE-002. Already settled\n')
        refs = [{'source': 'assumptions', 'label': 'Source'}]
        self.data = {'title': 'Community classes', 'subtitle': 'Find a class.', 'scope': 'Bookings only.', 'date': '2026-01-15', 'assumptions_source': 'assumptions', 'sources': {k: {'path':p, 'url':'https://example.org/'+p, 'label':k} for k,p in [('prd','class-bookings-prd.md'), ('assumptions','class-bookings-assumptions.md')]}, 'sections': [{'id':'booking','title':'Book a class','intro':'Choose a place.','rules':[],'mockups':[],'decisions':[{'id':ident,'title':title,'proposal':['Proposed behavior.'],'evidence':'The brief leaves this open.','refs':refs} for ident,title in [('RULE-001','Cancel before the class?'),('UI-001','Show a queue position?')]]}]}
        self.input = self.root / 'class-bookings-review.json'
        self.input.write_text(json.dumps(self.data))

    def test_complete_review_and_settled_exclusion(self):
        output = render(self.data, self.root, None)
        self.assertIn('id="RULE-001"', output)
        self.assertNotIn('id="RULE-002"', output)
        self.assertEqual(output.count('class="decision"'), 2)
        self.assertNotIn(' checked', output)
        self.assertIn('UNANSWERED', output)

    def test_missing_duplicate_and_unexpected_decisions_fail(self):
        for mode in ('missing','duplicate','extra'):
            data = copy.deepcopy(self.data)
            decisions = data['sections'][0]['decisions']
            if mode == 'missing': decisions.pop()
            if mode == 'duplicate': decisions.append(copy.deepcopy(decisions[0]))
            if mode == 'extra': decisions[0]['id'] = 'RULE-002'
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate(data, self.root)

    def test_unrecognized_inventory_is_not_silently_empty(self):
        (self.root / 'class-bookings-assumptions.md').write_text('# Open questions\n- Should cancellations be free?\n')
        with self.assertRaises(ValueError): validate(self.data, self.root)

    def test_unanswered_blocker_cannot_be_omitted_from_review(self):
        register = self.root / 'class-bookings-assumptions.md'
        register.write_text('## Blocking Open Questions\n### Blocking: Who may cancel a booking?\nNo option is favored.\n' + register.read_text())
        for explicit_inventory in (False, True):
            data = copy.deepcopy(self.data)
            if explicit_inventory:
                data.update(open_assumption_ids=['RULE-001', 'UI-001'], inventory_note='Checked the numbered entries.')
            with self.subTest(explicit_inventory=explicit_inventory), self.assertRaisesRegex(ValueError, 'Unanswered blocking question'):
                render(data, self.root, None)

    def test_plain_prose_cannot_inject_html_or_template_slots(self):
        self.data['sections'][0]['decisions'][0]['proposal'] = ['</script><img src=x onerror=alert(1)> @@TITLE@@']
        output = render(self.data, self.root, None)
        self.assertIn('&lt;/script&gt;&lt;img', output)
        self.assertIn('@@TITLE@@', output)
        self.assertNotIn('<img src=x', output)

    def test_changed_source_is_stale(self):
        before = manifest(self.data, self.root)
        (self.root / 'class-bookings-prd.md').write_text('Cancellation behavior changed.')
        self.assertNotEqual(before, manifest(self.data, self.root))

    def test_embedded_image_bytes_are_part_of_snapshot_identity(self):
        image = self.root / 'class-screen.png'
        image.write_bytes(b'unit test raster bytes')
        self.data['sections'][0]['mockups'] = [{'id':'BOOK-1', 'file':image.name,
            'title':'Class selection','alt':'Class selection','caption':'Fictional fixture',
            'refs':[{'source':'prd','label':'AC-BOOK-01'}]}]
        first = render(self.data, self.root, self.root)
        extracted = EmbeddedImages()
        extracted.feed(first)
        self.assertEqual(extracted.hashes['BOOK-1'], digest(image.read_bytes()))
        image.write_bytes(b'changed unit test raster bytes')
        second = render(self.data, self.root, self.root)
        import re
        version = lambda text: re.search(r'Snapshot ([a-f0-9]+)', text)[1]
        self.assertNotEqual(version(first), version(second))

    def test_html_alone_supports_refresh_and_freshness_after_json_is_deleted(self):
        image = self.root / 'class-screen.png'
        image.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aF6kAAAAASUVORK5CYII='))
        self.data['sections'][0]['mockups'] = [{'id':'BOOK-1', 'file':image.name,
            'title':'Class selection','alt':'Class selection','caption':'Fictional fixture',
            'refs':[{'source':'prd','label':'AC-BOOK-01'}]}]
        self.input.write_text(json.dumps(self.data))
        output = self.root / 'class-bookings-stakeholder-review.html'
        script = Path(__file__).with_name('render_review.py')
        def run(input_path, check=False):
            command = [sys.executable, str(script), '--repo-root', str(self.root),
                       '--input', str(input_path), '--output', str(output), '--images-dir', str(self.root)]
            if check: command.append('--check')
            return subprocess.run(command, text=True, capture_output=True)
        first = run(self.input)
        self.assertEqual(first.returncode, 0, first.stderr)
        original = output.read_text()
        self.input.unlink()
        self.assertEqual(load_authoring(output), self.data)
        checked = run(output, check=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        rebuilt = run(output)
        self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr)
        self.assertEqual(output.read_text(), original)
        # Editing embedded authoring must be detected until the visible HTML is rebuilt.
        changed = copy.deepcopy(self.data)
        changed['sections'][0]['intro'] = 'A revised workflow explanation.'
        from render_review import json_safe
        output.write_text(original.replace(json_safe(self.data), json_safe(changed)))
        self.assertNotEqual(run(output, check=True).returncode, 0)
        rebuilt = run(output)
        self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr)
        self.assertIn('A revised workflow explanation.', output.read_text())
        self.assertEqual(load_authoring(output), changed)
        self.assertEqual(run(output, check=True).returncode, 0)
        # A real source change still invalidates the saved snapshot.
        (self.root / 'class-bookings-prd.md').write_text('Availability now shows the venue.')
        self.assertNotEqual(run(output, check=True).returncode, 0)
        self.assertEqual(run(output).returncode, 0)
        self.assertNotEqual(output.read_text(), original)
        # Reviewer answers are never approval carried into a rebuilt package.
        output.write_text(output.read_text().replace('id="saved-responses">null',
                         'id="saved-responses">{"reviewer":"Example","answers":{}}'))
        self.assertEqual(run(output).returncode, 0)
        self.assertIsNone(embedded_json(output.read_text(), 'saved-responses'))

    def test_embedded_authoring_roundtrips_safely_and_changes_invalidate_snapshot(self):
        self.data['subtitle'] = '</script><script>alert("example")</script> & café'
        output = self.root / 'class-bookings-stakeholder-review.html'
        output.write_text(render(self.data, self.root, None))
        self.assertEqual(load_authoring(output), self.data)
        proof = embedded_json(output.read_text(), 'source-manifest')
        self.assertEqual(proof['editorial'], authoring_digest(self.data))
        changed = copy.deepcopy(self.data)
        changed['sections'][0]['intro'] = 'A corrected workflow explanation.'
        self.assertNotEqual(proof['editorial'], authoring_digest(changed))
        self.assertNotIn('<script>alert(', output.read_text())

    def test_missing_duplicate_or_malformed_embedded_authoring_fails(self):
        output = self.root / 'class-bookings-stakeholder-review.html'
        for content in ('<html>Older review without authoring data.</html>',
                        '<script id="authoring-data">{}</script>' * 2,
                        '<script id="authoring-data">invalid</script>'):
            output.write_text(content)
            with self.subTest(content=content), self.assertRaises(ValueError):
                load_authoring(output)

    def test_unsafe_source_and_missing_reference_fail(self):
        for mode in ('url','path','ref'):
            data = copy.deepcopy(self.data)
            if mode == 'url': data['sources']['prd']['url'] = 'javascript:alert(1)'
            if mode == 'path': data['sources']['prd']['path'] = '../outside.md'
            if mode == 'ref': data['sections'][0]['decisions'][0]['refs'][0]['source'] = 'absent'
            with self.subTest(mode=mode), self.assertRaises(ValueError): validate(data, self.root)


if __name__ == '__main__':
    unittest.main()
