# The Enso Method Plugin Privacy Policy

Effective date: 2026-10-11.

This policy covers the official Enso Method agent skills published by
EnsoDynamics in this repository. It does not cover modified forks, software you
build with the skills, or the Enso Method website.

## What the plugin contains

The plugin is primarily a collection of written instructions and documentation.
It also includes two optional Python hook scripts described below. It has no MCP
servers, automatically enabled hooks, analytics or telemetry. It does not run an
EnsoDynamics service or send project data to an EnsoDynamics endpoint.

## Optional local hooks

The setup guide describes two scripts you can choose to configure in Claude
Code. Installing the plugin does not enable them automatically.

The documented configuration puts the hooks in your global Claude Code settings.
Once enabled there, they can process matching events in any Claude Code session,
including other projects and sessions where you have not invoked an Enso Method
skill. Remove their entries from those settings to disable them.

- The session-title hook reads the current prompt supplied by Claude Code and,
  when needed, the local session transcript to check whether a user message
  already exists. It returns a session title to Claude Code.
- The assumptions-document reminder reads the tool event's file path and session
  identifier. It returns a reminder to Claude Code when an assumptions document
  is edited, and writes an empty local temporary marker named with a hash of the
  session identifier and file path to avoid repeating the reminder.

Neither script makes network calls or sends information to EnsoDynamics. Claude
Code handles their returned title or reminder under its own settings and terms.
Temporary markers remain until removed by you or your system's temporary-file
cleanup.

## Data used during your work

Your coding agent follows the skills using the tools and permissions available
in your environment. Depending on the task you request, this can involve reading
project files, requirements and business records; querying databases and APIs;
and writing requirements, assumptions, code and other project documents. Those
inputs and outputs may contain personal or confidential information.

The implementation skills also direct the agent to create and read local
`.agent-sessions/` logs to coordinate work. These can include session identifiers,
chat titles, project and task names, status events, timestamps and worktree paths.
The instructions require excluding this folder from Git. When creating another
log, the agent is instructed to remove completed logs older than seven days and
logs untouched for fourteen days. This cleanup depends on the agent following
those instructions; it is not automatic expiry. Copies you retain, backups and
data processed by your AI provider follow their own retention settings.

The agent may use your configured credentials to access systems needed for your
task. The plugin provides no credential collection form or credential storage
service. Credentials, tool access and permission decisions remain part of your
agent and environment configuration.

Project data can be processed by the AI provider you use. If your requested work
uses external services, such as web research, APIs, remote testing or GitHub
pushes, those services can receive the information needed for those operations.
The plugin has no fixed remote service integration. Which services receive data
depends on your task, tools and configuration.

## What EnsoDynamics receives and retains

EnsoDynamics receives no project files, prompts, outputs or credentials through
the plugin and therefore has no copy of that data to retain, sell or delete.
This does not mean your agent or other services retain nothing. Workspace files,
chat records, service logs and remote repositories follow your configuration and
the terms of their respective providers.

If you contact EnsoDynamics for support, the information you choose to send,
including your contact details and report, is used to investigate and respond.
It is retained as needed to handle the report and any related security or legal
obligations. GitHub issues are public; do not put personal data, confidential
project details or credentials in them. Use the private security reporting
channel for sensitive reports.

## Other providers

Review the policies and account settings of the services you use. Common
examples are [Anthropic](https://www.anthropic.com/legal/privacy),
[OpenAI](https://openai.com/policies/privacy-policy/) and
[GitHub](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
Their policies and any applicable business agreements govern their processing;
this plugin policy does not replace them or promise their retention settings.
Review other providers separately if you configure additional services.

## Questions and changes

For privacy questions or requests concerning information you sent directly to
EnsoDynamics, email doug@ensodynamics.com. For data held by your agent or another
provider, use that provider's controls or contact them directly.

Changes to this policy are published in this repository with an updated
effective date. Previous versions remain available in Git history.
