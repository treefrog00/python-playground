### Installing

See parent folder README on google auth, direnv and uv, then:

```bash
crewai install
```

## Running the Project

To kickstart your flow and begin execution, run this from the root folder of your project:

```bash
crewai flow kickoff
```

or

```bash
crewai run
```

### AgentOps

Add a AGENTOPS_API_KEY to .env to enable agent ops tracing. There is a line in `main.py` that initializes it with `agentops.init()`.