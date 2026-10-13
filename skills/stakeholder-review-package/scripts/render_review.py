#!/usr/bin/env python3
"""Build a standalone, source-traceable stakeholder review. Standard library only."""
import argparse
import base64
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, quote

SKILL = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL / 'assets' / 'stakeholder-review.html'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def esc(value):
    return html.escape(str(value), quote=True)


def json_safe(value):
    return json.dumps(value, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


def authoring_digest(data):
    # Hash the authoring content, not the HTML containing its own manifest.
    return digest(json.dumps(data, sort_keys=True, ensure_ascii=True).encode())


def embedded_json(text, ident):
    blocks = re.findall(r'<script\b[^>]*\bid="' + re.escape(ident) + r'"[^>]*>(.*?)</script>', text, re.S)
    if len(blocks) != 1:
        raise ValueError(f'Expected exactly one embedded {ident} block; older reviews need their original authoring JSON for a one-time rebuild')
    return json.loads(blocks[0])


def load_authoring(path):
    text = path.read_text()
    if path.suffix.lower() in ('.html', '.htm'):
        return embedded_json(text, 'authoring-data')
    if path.suffix.lower() == '.json':
        return json.loads(text)
    raise ValueError('Authoring input must be a review HTML file or temporary JSON file')


def open_ids(text):
    active = re.split(r'^##\s+Validated Assumptions\s*$', text, flags=re.M | re.I)[0]
    return re.findall(r'^#{2,6}\s+([A-Z][A-Z0-9]*-\d{3})[.\s:]', active, re.M)


def validate(data, root):
    sources = data['sources']
    for source in sources.values():
        path = Path(source['path'])
        if path.is_absolute() or not (root / path).resolve().is_relative_to(root.resolve()):
            raise ValueError('Source paths must stay inside the repository')
        if urlsplit(source['url']).scheme != 'https' or not urlsplit(source['url']).netloc:
            raise ValueError('Sources need HTTPS URLs')
        (root / path).read_bytes()
    register = (root / sources[data['assumptions_source']]['path']).read_text()
    active = re.split(r'^##\s+Validated Assumptions\s*$', register, flags=re.M | re.I)[0]
    if re.search(r'^#{2,6}\s+Blocking\s*:', active, re.M | re.I):
        raise ValueError('Unanswered blocking question: resolve it in the assumptions source before creating a Confirm/Change review; do not invent a proposal or omit it')
    expected = open_ids(register)
    if 'open_assumption_ids' in data:
        if not data.get('inventory_note'):
            raise ValueError('An explicit inventory requires inventory_note')
        expected = data['open_assumption_ids']
    elif not expected:
        raise ValueError('No open IDs parsed; check register format and supply an explicit inventory')
    actual, section_ids, screen_ids = [], [], []
    for section in data['sections']:
        sid = section['id']
        if not re.fullmatch('[a-z][a-z0-9-]*', sid):
            raise ValueError('Section IDs must be lowercase slugs')
        section_ids.append(sid)
        for item in section['rules'] + section['mockups'] + section['decisions']:
            if not item['refs']:
                raise ValueError('Every item needs source references')
            for ref in item['refs']:
                if ref['source'] not in sources:
                    raise ValueError('Unknown source: ' + ref['source'])
        for item in section['decisions']:
            if not re.fullmatch(r'[A-Z][A-Z0-9]*-\d{3}', item['id']):
                raise ValueError('Decision IDs must match the source ID format')
            actual.append(item['id'])
            if not item['title'] or not item['proposal'] or not all(item['proposal']):
                raise ValueError('Each decision needs a title and proposal')
            if not item['evidence']:
                raise ValueError('Each decision needs supporting context')
        for item in section['mockups']:
            screen_ids.append(item['id'])
            if item.get('focus', 'top') not in ('top', 'bottom'):
                raise ValueError('Screen focus must be top or bottom')
            if Path(item['file']).name != item['file']:
                raise ValueError('Mockup files must be basenames')
    for values in (expected, actual, section_ids, screen_ids):
        if len(values) != len(set(values)):
            raise ValueError('Duplicate IDs are not allowed')
    if set(expected) != set(actual):
        raise ValueError(f'Assumption coverage differs: missing={sorted(set(expected)-set(actual))}, extra={sorted(set(actual)-set(expected))}')


def manifest(data, root, images=None):
    return {
        'sources': {s['path']: digest((root / s['path']).read_bytes()) for s in data['sources'].values()},
        'editorial': authoring_digest(data),
        'template': digest(TEMPLATE.read_bytes()),
        'renderer': digest(Path(__file__).read_bytes()),
        'images': images if images is not None else {},
    }


def refs_markup(refs, sources):
    links = []
    for ref in refs:
        url = sources[ref['source']]['url']
        if ref.get('anchor'):
            url += '#' + quote(ref['anchor'], safe='-._~')
        links.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(ref["label"])}</a>')
    return '<span class="source-links">' + ' · '.join(links) + '</span>'


def render(data, root, images_dir):
    validate(data, root)
    image_hashes = {screen['id']: digest((images_dir / screen['file']).read_bytes())
                    for section in data['sections'] for screen in section['mockups']}
    proof = manifest(data, root, image_hashes)
    version = digest(json.dumps(proof, sort_keys=True).encode())[:12]
    sources = data['sources']
    navigation, sections = [], []
    decisions = []
    for index, section in enumerate(data['sections'], 1):
        sid = section['id']
        navigation.append(f'<a href="#{sid}"><span class="nav-number">{index:02}</span><span>{esc(section["title"])}</span><span class="section-count" data-section="{sid}"></span></a>')
        rules = ''.join(f'<li>{esc(r["text"])} {refs_markup(r["refs"], sources)}</li>' for r in section['rules'])
        gallery = []
        for screen in section['mockups']:
            image_path = images_dir / screen['file']
            mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}[image_path.suffix.lower()]
            uri = f'data:{mime};base64,' + base64.b64encode(image_path.read_bytes()).decode()
            gallery.append(f'<figure id="screen-{esc(screen["id"])}"><div class="screen-preview" tabindex="0" role="region" aria-label="{esc(screen["title"])} preview; scroll to see more" data-focus="{screen.get("focus", "top")}"><img src="{uri}" alt="{esc(screen["alt"])}" loading="lazy"></div><figcaption><strong>{esc(screen["title"])}</strong><p>{esc(screen["caption"])}</p>{refs_markup(screen["refs"], sources)} <button type="button" class="text-button enlarge enhanced" aria-label="Enlarge {esc(screen["title"])}">Enlarge</button></figcaption></figure>')
        cards = []
        for item in section['decisions']:
            ident = item['id']
            decisions.append({**item, 'section': sid})
            importance = f'<span class="attention">{esc(item["attention"])}</span>' if item.get('attention') else ''
            proposal = ''.join(f'<p>{esc(p)}</p>' for p in item['proposal'])
            options = ''.join(f'<label><input type="radio" name="{ident}" value="{value}"><span>{label}</span></label>' for value, label in [('confirm', 'Confirm'), ('change', 'Change')])
            confidence = f'<p class="confidence">Source confidence: {esc(item["confidence"])}</p>' if item.get('confidence') else ''
            cards.append(f'''<article class="decision" id="{ident}" data-section="{sid}">
<div class="decision-top"><span class="decision-id">{ident}</span>{importance}<span class="answer-status">Unanswered</span><button type="button" class="clear-answer text-button" aria-label="Clear response to {ident}" hidden>Clear</button></div>
<h3>{esc(item['title'])}</h3><div class="proposal">{proposal}</div>
<details class="evidence"><summary>Why this is proposed</summary><p>{esc(item['evidence'])}</p>{confidence}{refs_markup(item['refs'], sources)}</details>
<fieldset><legend>Your response to {ident}</legend><div class="choices">{options}</div></fieldset>
<label class="comment-label" for="comment-{ident}">Correction or comment <span>(optional for confirmation)</span></label>
<textarea id="comment-{ident}" rows="2" placeholder="Describe the change, or what you’re unsure about."></textarea>
</article>''')
        screens = '<div class="gallery">' + ''.join(gallery) + '</div>' if gallery else ''
        sections.append(f'''<section class="workflow" id="{sid}"><header class="section-heading"><span class="eyebrow">{index:02} / THE WORKFLOW</span><h2>{esc(section['title'])}</h2><p>{esc(section['intro'])}</p></header>
<div class="workflow-layout"><div class="context"><h3 class="column-heading">Key requirements &amp; mockups</h3><div class="context-content"><ul class="rules">{rules}</ul>{screens}</div>
<div class="workflow-feedback"><label for="note-{sid}">Feedback on requirements or mockups</label><p id="note-help-{sid}">What should work or look differently in this part of the workflow?</p><textarea id="note-{sid}" rows="3" aria-describedby="note-help-{sid}" placeholder="Optional — describe the requirement or screen and your suggested change"></textarea></div></div>
<div class="decisions"><h3 class="column-heading">Assumptions to confirm</h3>{''.join(cards)}</div></div></section>''')
    source_links = ' · '.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["label"])}</a>' for s in sources.values() if s.get('show', True))
    payload = {'title': data['title'], 'version': version, 'date': data['date'], 'decisions': decisions, 'sections': [{'id':s['id'],'title':s['title']} for s in data['sections']], 'sources':sources}
    replacements = {'TITLE': esc(data['title']), 'SUBTITLE': esc(data['subtitle']), 'SCOPE': esc(data['scope']), 'DATE':esc(data['date']), 'VERSION':version, 'COUNT':str(len(decisions)), 'NAV':''.join(navigation), 'SECTIONS':''.join(sections), 'SOURCE_LINKS': source_links, 'DATA':json_safe(payload), 'MANIFEST':json_safe(proof), 'AUTHORING':json_safe(data)}
    output = TEMPLATE.read_text()
    # One pass: authored text must never become another template substitution.
    return re.sub(r'@@([A-Z_]+)@@', lambda m: replacements[m[1]], output)


class EmbeddedImages(HTMLParser):
    """Identify the actual raster bytes in each generated screen figure."""
    def __init__(self):
        super().__init__()
        self.current = None
        self.hashes = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'figure' and attrs.get('id', '').startswith('screen-'):
            self.current = attrs['id'][7:]
        elif tag == 'img' and self.current:
            if self.current in self.hashes:
                raise ValueError('Duplicate embedded screen image')
            header, encoded = attrs['src'].split(',', 1)
            if not header.startswith('data:image/') or not header.endswith(';base64'):
                raise ValueError('Review images must be embedded raster data')
            self.hashes[self.current] = digest(base64.b64decode(encoded, validate=True))

    def handle_endtag(self, tag):
        if tag == 'figure':
            self.current = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', required=True, type=Path)
    parser.add_argument('--input', required=True, type=Path, help='Existing review HTML, or temporary authoring JSON for its first build')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--images-dir', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = load_authoring(args.input)
    validate(data, args.repo_root)
    if args.check:
        output = args.output.read_text()
        proof = embedded_json(output, 'source-manifest')
        stored_data = embedded_json(output, 'authoring-data')
        if authoring_digest(stored_data) != authoring_digest(data):
            raise SystemExit('STALE: embedded authoring data differs from the input; rebuild before sharing.')
        images = EmbeddedImages()
        images.feed(output)
        if args.images_dir is not None:
            current_images = {screen['id']: digest((args.images_dir / screen['file']).read_bytes())
                              for section in data['sections'] for screen in section['mockups']}
            if current_images != images.hashes:
                raise SystemExit('STALE: embedded images differ from current captures; rebuild.')
        if proof != manifest(data, args.repo_root, images.hashes):
            raise SystemExit('STALE: sources, editorial input or rendering assets changed; rebuild before sharing.')
        print('Freshness OK: current sources and rendering assets match this snapshot.')
    else:
        if any(s['mockups'] for s in data['sections']) and args.images_dir is None:
            parser.error('--images-dir is required when mockups are included')
        output = render(data, args.repo_root, args.images_dir)
        args.output.write_text(output)
        print(f'Built {args.output.name}: {len(output.encode())} bytes; all open assumptions covered.')


if __name__ == '__main__':
    main()
