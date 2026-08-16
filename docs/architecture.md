# AgentTrust-OS Architecture

## Product

AgentTrust-OS is one unified fintech application with two roles:

- User
- Banker

The same application supports:

- English
- Hindi

Users select their role during login and receive the appropriate workspace.

---

## System Structure

```text
                    AgentTrust-OS
                          |
              +-----------+-----------+
              |                       |
            User                    Banker
              |                       |
              +-----------+-----------+
                          |
                      Frontend
                     Member 2
                          |
                     API Layer
                          |
              +-----------+-----------+
              |                       |
           Backend                    AI
          Member 1                 Member 3
              |                       |
              +-----------+-----------+
                          |
                       Database