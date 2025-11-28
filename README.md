# Agentic Query Assistant - Enhanced Agent Architecture

## Overview

This is an enhanced agentic AI system that processes user queries through a structured perception-decision-action loop with advanced features including human-in-the-loop intervention, performance monitoring, and robust error handling.

## Architecture Evolution

### Previous Architecture (Base Version)
The original architecture followed a simple linear flow:
```
User Query → Perception → Decision → Action → Response
```

**Components:**
- **Perception Module**: Analyzed user queries and context
- **Decision Module**: Generated execution plans and steps
- **Action Module**: Executed code and tool calls
- **Memory System**: Basic session logging and memory search
- **MCP Integration**: Multi-server tool execution

**Limitations:**
- No failure recovery mechanisms
- Unlimited step execution
- No human intervention capabilities
- Basic error handling
- No performance monitoring

### Enhanced Architecture (Current Version)

The enhanced architecture introduces several critical improvements:

```
User Query → Perception → Decision → Action → Evaluation
     ↑           ↓           ↓        ↓         ↓
Human-In-Loop ← Failure Detection ← Performance Monitor
     ↑                              ↓
Plan Suggestion ← Max Steps/Retries Control
```

## Key Architectural Changes

### 1. Human-In-Loop Integration
**Previous**: Automatic failure handling with basic error messages
**Enhanced**: Interactive human intervention system

- **Tool Failure Intervention**: When tools fail, the system pauses and requests human input
- **Plan Failure Recovery**: Failed plans trigger human consultation with suggested alternatives
- **Interactive Decision Making**: Humans can override agent decisions at critical points

### 2. Execution Control Mechanisms
**Previous**: Unlimited execution with basic timeouts
**Enhanced**: Strict execution boundaries

- **Max Steps Limit**: Hard limit of 3 steps per execution cycle
- **Max Retries Control**: Maximum of 3 retry attempts per failed operation
- **Graceful Degradation**: System provides meaningful feedback when limits are reached

### 3. Performance Monitoring System
**Previous**: Basic execution logging
**Enhanced**: Comprehensive performance tracking

- **Tool Performance Logging**: Detailed metrics for each tool execution
- **Performance Feedback Loop**: Historical performance data influences future decisions
- **Multi-execution Analysis**: Performance patterns across multiple runs

### 4. Advanced Testing Infrastructure
**Previous**: Manual testing only
**Enhanced**: Automated testing suite

- **Simulator Framework**: Runs 100+ automated test scenarios
- **Rate Limiting**: Built-in sleep delays to prevent API bans
- **Comprehensive Coverage**: Tests various failure modes and edge cases

## System Components

### Core Modules

#### 1. Agent Loop (`agent/agent_loop2.py`)
- **Enhanced Features**: Human-in-loop integration, step/retry limits
- **Responsibilities**: Main execution orchestration, failure detection, human intervention triggers

#### 2. Perception Module (`perception/perception.py`)
- **Enhanced Features**: Context-aware analysis with performance history
- **Responsibilities**: Query understanding, context extraction, goal assessment

#### 3. Decision Module (`decision/decision.py`)
- **Enhanced Features**: Performance-informed planning, failure-aware decision making
- **Responsibilities**: Plan generation, step creation, adaptive replanning

#### 4. Action Executor (`action/executor.py`)
- **Enhanced Features**: Performance logging, failure detection, timeout management
- **Responsibilities**: Code execution, tool orchestration, result processing

#### 5. Human-In-Loop Handler (`agent/human_in_loop.py`) - **NEW**
- **Features**: Interactive prompts, suggestion generation, decision validation
- **Responsibilities**: Human interaction management, fallback handling

#### 6. Performance Monitor (`monitoring/performance_monitor.py`) - **NEW**
- **Features**: Tool performance tracking, historical analysis, feedback generation
- **Responsibilities**: Performance data collection, analysis, reporting

#### 7. Test Simulator (`testing/simulator.py`) - **NEW**
- **Features**: Automated test execution, scenario generation, result analysis
- **Responsibilities**: Comprehensive testing, performance validation

### Data Flow

1. **Query Processing**
   ```
   User Query → Perception (with performance context) → Enhanced Understanding
   ```

2. **Decision Making**
   ```
   Understanding → Decision (with historical data) → Performance-Informed Plan
   ```

3. **Execution with Monitoring**
   ```
   Plan → Action (with logging) → Performance Data → Feedback Loop
   ```

4. **Failure Handling**
   ```
   Failure Detection → Human-In-Loop → Alternative Suggestion → Recovery
   ```

## Configuration

### Execution Limits
```python
MAX_STEPS = 3           # Maximum steps per execution cycle
MAX_RETRIES = 3         # Maximum retry attempts per operation
TIMEOUT_PER_STEP = 30   # Seconds per step execution
```

### Human-In-Loop Settings
```python
ENABLE_HUMAN_INTERVENTION = True    # Enable human-in-loop features
AUTO_SUGGEST_ALTERNATIVES = True    # Generate alternative plans
INTERVENTION_TIMEOUT = 300          # Seconds to wait for human input
```

### Performance Monitoring
```python
ENABLE_PERFORMANCE_LOGGING = True   # Enable performance tracking
PERFORMANCE_HISTORY_LIMIT = 1000    # Number of executions to track
FEEDBACK_THRESHOLD = 0.7            # Performance threshold for feedback
```

## Usage Examples

### Basic Query Processing
```python
agent = AgentLoop(
    perception_prompt_path="prompts/perception_prompt.txt",
    decision_prompt_path="prompts/decision_prompt.txt",
    multi_mcp=multi_mcp,
    strategy="exploratory",
    max_steps=3,
    max_retries=3
)

response = await agent.run("What is the weather in New York?")
```

### Human-In-Loop Intervention
```python
# When a tool fails, the system will:
# 1. Detect the failure
# 2. Present the error to the human
# 3. Request guidance or alternative approach
# 4. Continue with human-provided solution

response = await agent.run_with_human_fallback("Complex query requiring intervention")
```

### Performance Analysis
```python
# Access performance data
performance_data = agent.get_performance_metrics()
print(f"Average tool execution time: {performance_data['avg_execution_time']}")
print(f"Success rate: {performance_data['success_rate']}")
```

### Automated Testing
```python
# Run comprehensive test suite
simulator = TestSimulator()
results = await simulator.run_test_suite(num_tests=100, delay_between_tests=1.0)
print(f"Test results: {results['summary']}")
```

## Key Improvements Summary

1. **Reliability**: Human-in-loop ensures no query goes unanswered
2. **Performance**: Monitoring and feedback improve execution quality
3. **Safety**: Step and retry limits prevent infinite loops
4. **Testability**: Automated testing ensures system robustness
5. **Observability**: Comprehensive logging and monitoring
6. **Adaptability**: Performance feedback influences future decisions

## Dependencies

- `google-genai`: LLM integration
- `pydantic`: Data validation
- `asyncio`: Asynchronous execution
- `yaml`: Configuration management
- `uuid`: Session identification
- `datetime`: Timestamp management

## Future Enhancements

- Machine learning-based performance optimization
- Advanced human-in-loop interfaces (GUI, voice)
- Distributed execution capabilities
- Real-time performance dashboards
- Integration with external monitoring systems

---

*This enhanced architecture provides a robust, monitored, and human-supervised agentic system capable of handling complex queries with high reliability and performance.*
