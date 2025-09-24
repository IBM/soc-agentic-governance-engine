# soc-agentic-governance-engine SAGE

Security Operations Centers (SOCs) are traditionally measured by their ability to detect and respond to threats. Yet, one of their most consistent and time-consuming challenges comes not from adversaries, but from compliance auditors. Frameworks like SOC 2, ISO 27001, and PCI-DSS require constant evidence collection across multiple tools, systems, and workflows.

Collecting this evidence manually can take 1–2 weeks per audit, consume valuable analyst bandwidth, and increase the risk of errors. For Managed Security Service Providers (MSSPs), who often juggle dozens of concurrent audits, the burden is even heavier.

SAGE (SOC Agentic Governance Engine) is designed to change that. By combining agentic AI with deep integrations into tools like QRadar, Resilient, and ServiceNow, SAGE automates audit evidence collection, interpretation, and reporting — reducing weeks of work into hours.


SAGE’s workflow is driven by a Supervisor Agent that orchestrates specialized sub-agents to handle different aspects of audit evidence collection:

    1.	Kick Off Audit Process – The user initiates the process by selecting the prompt “Kick Off Audit Process.”

    2.	File Upload Agent –
        o	Provides a file upload option in the chat interface.
        o	Reads the uploaded Excel audit checklist.
        o	Displays the file contents within the chat.
        o	Forwards the extracted data to the API Extractor Agent.

    3.	API Extractor Agent –
        o	Built with Langflow and exported as an MCP server. "QRadarAPIDocExtraction.json" is that MCP server only where user needs to update their PROJECT_ID, API_KEY and WATSOX_URL
        o	Interprets checklist requirements written in plain language.
        o	References QRadar API documentation to identify the correct API endpoint(s).
        o	Returns endpoint details to the Supervisor Agent.

    4.	AQL Query Agent –
        o	Invoked when a checklist item relates to log source or event data.
        o	Executes Ariel Query Language (AQL) queries via QRadar APIs.
        o	Retrieves logs tied to specific audit requirements.

    5.	QRadar API Executor Agent –
        o	Executes the API endpoint(s) identified by the API Extractor Agent.
        o	Displays responses directly in the chat interface.

    6.	Supervisor Agent –
        o	Orchestrates the overall process, delegating tasks across sub-agents.
        o	Aggregates outputs from the AQL Query Agent and API Executor Agent.
        o	Synthesizes a final, structured response.
        o	Presents an audit-ready summary with evidence, metadata, and mappings back to compliance controls.
