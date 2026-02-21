# Changelog

All notable changes to the THUNDERFIRE Python SDK will be documented in this file.

## [1.0.0] - 2026-02-21

### Added
- **Core Client** - Async/sync THUNDERFIRE API client
- **LangChain Integration** - ThunderFireToolkit with 16 tools
- **CrewAI Integration** - ThunderFireTools for multi-agent crews
- **AutoGen Integration** - Tool registration for ConversableAgent
- **OpenAI Integration** - Function definitions for GPT models
- **MCP Server** - Model Context Protocol server (CLI + library)
- **Demo Dashboard** - Terminal-based monitoring example

### Tools Available
- `thunderfire_node_list` - List connected nodes
- `thunderfire_node_health` - CHITRAL health status
- `thunderfire_node_create` - Create new node
- `thunderfire_marketplace_search` - Search TF Store
- `thunderfire_marketplace_install` - Install package
- `thunderfire_chitral_decode` - Decode hex message
- `thunderfire_chitral_status` - Live CHITRAL status
- `thunderfire_theta_run` - Execute THETA cycle
- `thunderfire_theta_status` - THETA pipeline status
- `thunderfire_service_discover` - Discover NOP services
- `thunderfire_service_request` - Request service
- `thunderfire_gym_tasks` - List GYM tasks
- `thunderfire_gym_complete` - Complete task
- `thunderfire_msg_send` - Send message
- `thunderfire_msg_history` - Message history
- `thunderfire_script_eval` - Execute TOP Script

[1.0.0]: https://github.com/mayayaiinfra/tf-python/releases/tag/v1.0.0
