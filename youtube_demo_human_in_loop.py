"""
YouTube Demo: Human-In-Loop Intervention on Tool Failure
==========================================================

This demo script demonstrates the human-in-loop feature by:
1. Artificially triggering a tool failure
2. Showing the intervention system in action
3. Demonstrating the suggestion mechanism
4. Showing the recovery process

Run with: python3 youtube_demo_human_in_loop.py
"""

import asyncio
import time
from typing import Dict, Any, List
from agent.human_in_loop import HumanInLoopHandler, InterventionContext, InterventionType


class DemoToolExecutor:
    """Simulates tool execution with controlled failures for demo purposes"""
    
    def __init__(self, force_failure: bool = False):
        self.force_failure = force_failure
        self.execution_count = 0
    
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool - can be forced to fail for demo"""
        self.execution_count += 1
        
        print(f"\n{'='*60}")
        print(f"🔧 EXECUTING TOOL: {tool_name}")
        print(f"{'='*60}")
        print(f"Parameters: {params}")
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        if self.force_failure:
            print("❌ TOOL EXECUTION FAILED!")
            return {
                "success": False,
                "error": f"Network timeout: Unable to connect to {tool_name} service",
                "error_code": "NETWORK_TIMEOUT",
                "retry_count": 2
            }
        else:
            print("✅ TOOL EXECUTION SUCCESSFUL!")
            return {
                "success": True,
                "result": f"Successfully executed {tool_name}",
                "data": {"value": 42}
            }


async def demo_scenario_1_tool_failure():
    """
    DEMO SCENARIO 1: Tool Failure with Human Intervention
    
    This scenario shows:
    - A tool that fails to execute
    - Human-in-loop intervention triggered
    - Intelligent suggestions provided
    - User choosing an alternative approach
    """
    
    print("\n" + "🎬 "*30)
    print("YOUTUBE DEMO: HUMAN-IN-LOOP INTERVENTION")
    print("🎬 "*30)
    
    print("\n📋 SCENARIO 1: Tool Failure with Human Intervention")
    print("-" * 60)
    
    # Initialize components
    human_handler = HumanInLoopHandler(timeout_seconds=300, enable_suggestions=True)
    tool_executor = DemoToolExecutor(force_failure=True)  # Force failure for demo
    
    # Demo query
    query = "Search for the latest AI research papers on arXiv"
    session_id = "demo-session-001"
    
    print(f"\n🎯 User Query: {query}")
    print(f"🆔 Session ID: {session_id}")
    
    # Simulate executing a step that will fail
    print("\n" + "⏳ "*30)
    print("STEP 1: Attempting to search arXiv database...")
    print("⏳ "*30)
    
    failed_step = {
        "type": "TOOL_CALL",
        "description": "Search arXiv database for AI research papers",
        "tool": "arxiv_search",
        "params": {
            "query": "artificial intelligence",
            "max_results": 10,
            "sort_by": "submittedDate"
        }
    }
    
    # Execute the tool (will fail)
    result = await tool_executor.execute_tool("arxiv_search", failed_step["params"])
    
    if not result["success"]:
        print("\n🚨 TOOL FAILURE DETECTED!")
        print(f"Error: {result['error']}")
        print(f"Error Code: {result['error_code']}")
        
        # Create intervention context
        context = InterventionContext(
            intervention_type=InterventionType.TOOL_FAILURE,
            original_query=query,
            failed_step=failed_step,
            error_message=result['error'],
            current_plan=[
                "Search arXiv database for AI research papers",
                "Filter results by relevance score",
                "Extract paper titles and abstracts",
                "Format results for presentation"
            ],
            completed_steps=[],
            session_id=session_id
        )
        
        # Trigger human intervention
        print("\n" + "🤝 "*30)
        print("TRIGGERING HUMAN-IN-LOOP INTERVENTION...")
        print("🤝 "*30)
        
        intervention_result = human_handler.handle_tool_failure(context)
        
        # Process the human's decision
        print("\n" + "📊 "*30)
        print("PROCESSING HUMAN DECISION...")
        print("📊 "*30)
        
        print(f"\n✅ Human Decision: {intervention_result['action']}")
        
        if intervention_result['action'] == "alternative":
            print(f"💡 Alternative Approach: {intervention_result['alternative_approach']}")
            print("\n🔄 Continuing execution with alternative approach...")
            
            # Simulate successful execution with alternative
            tool_executor.force_failure = False
            new_result = await tool_executor.execute_tool(
                "google_scholar_search", 
                {"query": "AI research papers"}
            )
            
            if new_result["success"]:
                print("\n🎉 SUCCESS! Query completed with alternative approach.")
                print(f"Result: {new_result['result']}")
        
        elif intervention_result['action'] == "retry":
            print(f"🔄 Retrying with modifications: {intervention_result['modifications']}")
            print("\n🔄 Attempting retry...")
        
        elif intervention_result['action'] == "skip":
            print("\n⏭️  Skipping failed step and continuing with next step...")
        
        elif intervention_result['action'] == "abort":
            print("\n🛑 Execution aborted by human decision.")
        
        # Show intervention summary
        print("\n" + "📈 "*30)
        print("INTERVENTION SUMMARY")
        print("📈 "*30)
        summary = human_handler.get_intervention_summary()
        print(f"Total Interventions: {summary['total_interventions']}")
        print(f"Intervention Types: {summary['intervention_types']}")
        print(f"Success Rate: {summary['success_rate']*100:.1f}%")


async def demo_scenario_2_automated_suggestions():
    """
    DEMO SCENARIO 2: Different Types of Tool Failures
    
    Shows how the system provides intelligent suggestions based on:
    - Type of failure
    - Step description
    - Query context
    """
    
    print("\n\n" + "🎬 "*30)
    print("SCENARIO 2: Intelligent Suggestion System")
    print("🎬 "*30)
    
    human_handler = HumanInLoopHandler(enable_suggestions=True)
    
    failure_scenarios = [
        {
            "name": "Code Execution Failure",
            "step": {
                "type": "CODE",
                "description": "Execute Python code to analyze data"
            },
            "error": "SyntaxError: invalid syntax on line 42"
        },
        {
            "name": "Search Tool Failure",
            "step": {
                "type": "TOOL_CALL",
                "description": "Search for scientific papers in database"
            },
            "error": "SearchError: Database connection timeout"
        },
        {
            "name": "Calculation Failure",
            "step": {
                "type": "CALCULATION",
                "description": "Calculate statistical metrics for dataset"
            },
            "error": "ValueError: Input data format mismatch"
        }
    ]
    
    for scenario in failure_scenarios:
        print(f"\n{'='*60}")
        print(f"🔍 Testing: {scenario['name']}")
        print(f"{'='*60}")
        
        context = InterventionContext(
            intervention_type=InterventionType.TOOL_FAILURE,
            original_query="Demo query for suggestion testing",
            failed_step=scenario["step"],
            error_message=scenario["error"],
            session_id="demo-suggestions"
        )
        
        suggestions = human_handler._generate_tool_failure_suggestions(context)
        
        print(f"Step Type: {scenario['step']['type']}")
        print(f"Error: {scenario['error']}")
        print("\n💡 Generated Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        
        await asyncio.sleep(0.5)


async def demo_scenario_3_visual_flow():
    """
    DEMO SCENARIO 3: Complete Visual Flow
    
    Shows the complete workflow with clear visual markers:
    - Normal execution
    - Failure detection
    - Human intervention
    - Recovery
    """
    
    print("\n\n" + "🎬 "*30)
    print("SCENARIO 3: Complete Visual Workflow")
    print("🎬 "*30)
    
    steps_to_visualize = [
        {"status": "✅", "name": "Perception", "message": "Query analyzed successfully"},
        {"status": "✅", "name": "Decision", "message": "Execution plan generated"},
        {"status": "⏳", "name": "Action - Step 1", "message": "Executing: Fetch weather data"},
        {"status": "✅", "name": "Action - Step 1", "message": "Weather data retrieved"},
        {"status": "⏳", "name": "Action - Step 2", "message": "Executing: Process temperature data"},
        {"status": "❌", "name": "Action - Step 2", "message": "FAILED: API rate limit exceeded"},
        {"status": "🤝", "name": "Human Intervention", "message": "Requesting human guidance..."},
        {"status": "💡", "name": "Suggestions", "message": "3 alternative approaches provided"},
        {"status": "👤", "name": "Human Decision", "message": "Selected: Use cached data"},
        {"status": "🔄", "name": "Recovery", "message": "Resuming with alternative approach"},
        {"status": "✅", "name": "Action - Step 2 (retry)", "message": "Successfully processed cached data"},
        {"status": "✅", "name": "Complete", "message": "Query successfully answered!"}
    ]
    
    for i, step in enumerate(steps_to_visualize, 1):
        print(f"\n[{i:02d}] {step['status']} {step['name']}")
        print(f"     └─ {step['message']}")
        await asyncio.sleep(0.8)
    
    print("\n" + "🎉 "*30)
    print("WORKFLOW COMPLETE - HUMAN-IN-LOOP SUCCESSFUL!")
    print("🎉 "*30)


async def interactive_demo():
    """
    INTERACTIVE DEMO: Live Human-In-Loop Test
    
    Allows the user to actually interact with the system
    """
    
    print("\n\n" + "🎮 "*30)
    print("INTERACTIVE DEMO: Try It Yourself!")
    print("🎮 "*30)
    
    print("\nThis will trigger a real tool failure and ask for your input.")
    print("You'll see exactly what happens during human intervention.")
    
    proceed = input("\n▶️  Press Enter to start interactive demo (or 'skip' to skip): ")
    
    if proceed.lower() == 'skip':
        print("⏭️  Skipping interactive demo...")
        return
    
    # Run actual interactive scenario
    await demo_scenario_1_tool_failure()


async def main():
    """Main demo execution"""
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║        YOUTUBE DEMO: HUMAN-IN-LOOP INTERVENTION                ║
    ║                                                                ║
    ║        Enhanced Agentic System with Failure Recovery           ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📺 This demo will show you:")
    print("  1. ✅ Tool failure detection")
    print("  2. 🤝 Human-in-loop intervention trigger")
    print("  3. 💡 Intelligent suggestion generation")
    print("  4. 🔄 Recovery and continuation")
    print("  5. 📊 Performance tracking")
    
    input("\n▶️  Press Enter to begin demo...")
    
    # Run demo scenarios
    try:
        # Scenario 1: Main tool failure demo
        await demo_scenario_1_tool_failure()
        
        input("\n▶️  Press Enter to continue to Scenario 2...")
        
        # Scenario 2: Show different suggestion types
        await demo_scenario_2_automated_suggestions()
        
        input("\n▶️  Press Enter to continue to Scenario 3...")
        
        # Scenario 3: Visual workflow
        await demo_scenario_3_visual_flow()
        
        # Interactive demo
        await interactive_demo()
        
        # Final summary
        print("\n\n" + "🎬 "*30)
        print("DEMO COMPLETE!")
        print("🎬 "*30)
        
        print("""
        📝 KEY TAKEAWAYS:
        
        ✅ Human-in-loop ensures no query goes unanswered
        ✅ Intelligent suggestions guide recovery decisions
        ✅ Multiple intervention options (retry, skip, alternative, abort)
        ✅ Full transparency of failure context
        ✅ Graceful degradation instead of crashes
        
        🚀 The system is production-ready with robust failure handling!
        """)
        
    except KeyboardInterrupt:
        print("\n\n⛔ Demo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
