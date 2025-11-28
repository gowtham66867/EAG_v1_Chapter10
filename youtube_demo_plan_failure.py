"""
YouTube Demo: Human-In-Loop for PLAN FAILURE
==============================================

This demo shows what happens when an entire execution plan fails
(not just a tool failure, but the plan/strategy itself doesn't work).

This is more common with complex queries and shows the full power
of human-in-loop intervention for strategic decision-making.

Run with: python3 youtube_demo_plan_failure.py
"""

import asyncio
import time
from typing import Dict, Any, List


class PlanExecutionSimulator:
    """Simulates plan execution with ability to fail at the plan level"""
    
    def __init__(self):
        self.steps_completed = []
        self.steps_failed = []
    
    async def execute_step(self, step: Dict[str, Any], will_succeed: bool = True) -> Dict[str, Any]:
        """Execute a single step"""
        step_num = len(self.steps_completed) + len(self.steps_failed) + 1
        
        print(f"\n{'='*60}")
        print(f"⚙️  EXECUTING STEP {step_num}: {step['description']}")
        print(f"{'='*60}")
        print(f"Type: {step['type']}")
        print(f"Details: {step.get('details', 'N/A')}")
        
        # Simulate processing
        for i in range(3):
            print(f"{'.'* (i+1)} Processing", end='\r')
            await asyncio.sleep(0.5)
        
        print(" " * 50, end='\r')  # Clear line
        
        if will_succeed:
            print(f"✅ Step {step_num} COMPLETED")
            self.steps_completed.append(step)
            return {"success": True, "result": step.get('expected_result', 'Success')}
        else:
            print(f"❌ Step {step_num} FAILED")
            print(f"Reason: {step.get('failure_reason', 'Unknown error')}")
            self.steps_failed.append(step)
            return {"success": False, "error": step.get('failure_reason', 'Step failed')}


async def show_banner(title: str):
    """Display a styled banner"""
    border = "🎬 " * 30
    print(f"\n{border}")
    print(f"{title.center(180)}")
    print(f"{border}\n")


async def show_section(section_name: str):
    """Display a section header"""
    print(f"\n{'='*60}")
    print(f"📋 {section_name}")
    print(f"{'='*60}\n")


async def show_plan_failure_screen(query: str, current_plan: List[str], completed_steps: List[str], failure_reason: str):
    """Display the plan failure intervention screen"""
    print("\n" + "🚨 "*30)
    print("PLAN FAILURE - HUMAN INTERVENTION REQUIRED".center(180))
    print("🚨 "*30)
    
    print(f"\nSession ID: demo-plan-failure-001")
    print(f"Original Query: {query}")
    print(f"Failure Reason: {failure_reason}")
    
    await asyncio.sleep(1)
    
    print("\n📋 CURRENT PLAN (FAILED):")
    for i, step in enumerate(current_plan, 1):
        status = "✅" if i <= len(completed_steps) else "❌"
        print(f"  {status} Step {i}: {step}")
    
    await asyncio.sleep(1)
    
    print(f"\n✅ COMPLETED STEPS: {len(completed_steps)}/{len(current_plan)}")
    if completed_steps:
        for step in completed_steps[-3:]:
            print(f"  • {step}")
    
    await asyncio.sleep(1)
    
    print("\n💡 SUGGESTED ALTERNATIVE PLANS:")
    suggestions = [
        "Break the problem into smaller, more manageable sub-queries",
        "Use a completely different approach with simpler tools",
        "Gather prerequisite information first, then proceed",
        "Switch to a hybrid manual-automated workflow"
    ]
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")
        await asyncio.sleep(0.3)
    
    await asyncio.sleep(1)
    
    print("\n📝 AVAILABLE ACTIONS:")
    print("  1. Provide completely new plan")
    print("  2. Use suggested alternative plan")
    print("  3. Modify current plan")
    print("  4. Abort execution")


async def show_human_decision(choice: str, new_plan: List[str]):
    """Display human decision with thinking simulation"""
    print("\n" + "👤 "*30)
    print("HUMAN DECISION PROCESS".center(180))
    print("👤 "*30)
    
    print("\n⏰ Analyzing failed plan...")
    await asyncio.sleep(1.5)
    
    print(f"\n✅ Human Selected: Option {choice}")
    print(f"💭 New Strategy: Simplify approach and break into atomic steps")
    
    await asyncio.sleep(1)
    
    print("\n📋 NEW EXECUTION PLAN:")
    for i, step in enumerate(new_plan, 1):
        print(f"  {i}. {step}")
        await asyncio.sleep(0.4)


async def show_recovery_process():
    """Display the recovery and continuation process"""
    print("\n" + "🔄 "*30)
    print("PLAN RECOVERY PROCESS INITIATED".center(180))
    print("🔄 "*30)
    
    steps = [
        "Discarding failed plan...",
        "Validating new approach...",
        "Simplifying complexity...",
        "Breaking into atomic steps...",
        "Resuming execution with new strategy..."
    ]
    
    for step in steps:
        print(f"\n⚙️  {step}")
        await asyncio.sleep(0.8)


async def main_demo():
    """Main automated demo for plan failure"""
    
    # Banner
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                                                                        ║
    ║          YOUTUBE DEMO: PLAN FAILURE INTERVENTION                       ║
    ║                                                                        ║
    ║          When Entire Plans Fail, Humans Provide New Strategy          ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)
    
    await asyncio.sleep(2)
    
    # Introduction
    await show_banner("DEMO: COMPLEX QUERY WITH PLAN FAILURE")
    
    print("""
    📺 This demo demonstrates:
    
    ✅ Complex query planning
    🚨 Plan-level failure detection (not just tool failures)
    🤝 Human intervention for strategic replanning
    💡 Intelligent plan suggestions based on failure patterns
    🔄 Complete plan replacement and recovery
    📊 Successful completion after plan modification
    
    Scenario: Multi-step complex query that fails midway
    
    """)
    
    await asyncio.sleep(3)
    
    # Scenario Setup
    await show_section("SCENARIO: Complex Multi-Source Data Analysis")
    
    query = "Analyze the correlation between weather patterns and stock market performance for tech companies in Q4 2024"
    
    print(f"🎯 User Query: {query}")
    print(f"\n🧠 This is a COMPLEX query requiring:")
    print(f"   • Multiple data sources (weather APIs, financial APIs)")
    print(f"   • Data correlation analysis")
    print(f"   • Time series processing")
    print(f"   • Statistical computation")
    
    await asyncio.sleep(3)
    
    # Initial Plan
    await show_section("INITIAL EXECUTION PLAN")
    
    initial_plan = [
        "Fetch weather data for all major tech company locations (Q4 2024)",
        "Retrieve stock prices for top 50 tech companies (Q4 2024)",
        "Perform correlation analysis between weather and stock movements",
        "Generate statistical significance tests",
        "Create visualization and summary report"
    ]
    
    print("📋 Agent Generated Plan:")
    for i, step in enumerate(initial_plan, 1):
        print(f"   Step {i}: {step}")
        await asyncio.sleep(0.5)
    
    await asyncio.sleep(2)
    
    # Execution Phase
    await show_section("EXECUTION PHASE")
    
    simulator = PlanExecutionSimulator()
    
    # Step 1 - Succeeds
    step1 = {
        "description": "Fetch weather data for major tech hubs",
        "type": "API_CALL",
        "details": "Querying weather APIs for SF, Seattle, Austin, NYC",
        "expected_result": "Weather data retrieved for 4 locations"
    }
    await simulator.execute_step(step1, will_succeed=True)
    await asyncio.sleep(1.5)
    
    # Step 2 - Succeeds
    step2 = {
        "description": "Retrieve stock prices for tech companies",
        "type": "API_CALL",
        "details": "Fetching Q4 2024 data for 50 companies",
        "expected_result": "Stock price data retrieved"
    }
    await simulator.execute_step(step2, will_succeed=True)
    await asyncio.sleep(1.5)
    
    # Step 3 - FAILS (Complex correlation analysis)
    step3 = {
        "description": "Perform correlation analysis",
        "type": "COMPUTATION",
        "details": "Cross-correlating weather patterns with stock movements",
        "failure_reason": "Data dimensionality mismatch - weather data is hourly, stock data is daily. Cannot directly correlate without preprocessing."
    }
    result3 = await simulator.execute_step(step3, will_succeed=False)
    await asyncio.sleep(2)
    
    # Plan Failure Detected
    print("\n" + "⚠️ "*30)
    print("CRITICAL: PLAN FAILURE DETECTED".center(180))
    print("⚠️ "*30)
    
    print("\n❌ The current plan cannot continue:")
    print("   • Step 3 failed due to data incompatibility")
    print("   • Remaining steps depend on Step 3")
    print("   • The ENTIRE PLAN strategy is flawed")
    print("   • Simple retry won't work - need NEW APPROACH")
    
    await asyncio.sleep(3)
    
    # Human Intervention
    await show_plan_failure_screen(
        query=query,
        current_plan=initial_plan,
        completed_steps=[
            "Weather data fetched (4 locations, hourly data)",
            "Stock prices retrieved (50 companies, daily data)"
        ],
        failure_reason="Data format incompatibility - cannot correlate hourly weather with daily stock data"
    )
    
    await asyncio.sleep(3)
    
    # Human Decision
    new_plan = [
        "Aggregate hourly weather data to daily averages",
        "Normalize both datasets to same time granularity",
        "Perform simplified correlation on daily aggregates",
        "Focus on major weather events vs stock volatility",
        "Generate summary with caveats about data limitations"
    ]
    
    await show_human_decision(choice="2", new_plan=new_plan)
    
    await asyncio.sleep(2)
    
    # Recovery
    await show_recovery_process()
    
    await asyncio.sleep(2)
    
    # Execute New Plan
    await show_section("EXECUTING NEW PLAN")
    
    print("🔄 Resuming with simplified, compatible approach...\n")
    await asyncio.sleep(1)
    
    # New Step 1
    new_step1 = {
        "description": "Aggregate hourly weather to daily",
        "type": "DATA_PROCESSING",
        "details": "Converting hourly weather to daily averages",
        "expected_result": "Daily weather aggregates created"
    }
    await simulator.execute_step(new_step1, will_succeed=True)
    await asyncio.sleep(1)
    
    # New Step 2
    new_step2 = {
        "description": "Normalize datasets to daily granularity",
        "type": "DATA_PROCESSING",
        "details": "Aligning weather and stock data by date",
        "expected_result": "Datasets normalized"
    }
    await simulator.execute_step(new_step2, will_succeed=True)
    await asyncio.sleep(1)
    
    # New Step 3
    new_step3 = {
        "description": "Simplified correlation analysis",
        "type": "COMPUTATION",
        "details": "Daily correlation between weather and stock volatility",
        "expected_result": "Correlation coefficients computed"
    }
    await simulator.execute_step(new_step3, will_succeed=True)
    await asyncio.sleep(1)
    
    # Success!
    print("\n" + "🎉 "*30)
    print("SUCCESS! QUERY COMPLETED WITH NEW PLAN".center(180))
    print("🎉 "*30)
    
    print("\n✅ Analysis Results:")
    print("   • Weak negative correlation (-0.23) found")
    print("   • Extreme weather events show 15% higher volatility")
    print("   • Results include data limitation caveats")
    print("   • Summary report generated successfully")
    
    await asyncio.sleep(2)
    
    # Comparison
    await show_section("PLAN COMPARISON")
    
    print("❌ ORIGINAL PLAN (FAILED):")
    print("   • Tried to correlate incompatible data formats")
    print("   • Didn't account for granularity mismatch")
    print("   • Would have required complex interpolation")
    print("   • High risk of statistical errors")
    
    await asyncio.sleep(2)
    
    print("\n✅ NEW PLAN (SUCCEEDED):")
    print("   • Preprocessed data to compatible format")
    print("   • Simplified analysis scope")
    print("   • Acknowledged limitations upfront")
    print("   • Achieved core objective with caveats")
    
    await asyncio.sleep(2)
    
    # Workflow Visualization
    await show_section("COMPLETE WORKFLOW")
    
    workflow_steps = [
        ("✅", "Perception", "Complex query analyzed"),
        ("✅", "Decision", "Initial plan generated (5 steps)"),
        ("⏳", "Execution - Step 1", "Fetch weather data"),
        ("✅", "Execution - Step 1", "Weather data retrieved"),
        ("⏳", "Execution - Step 2", "Fetch stock data"),
        ("✅", "Execution - Step 2", "Stock data retrieved"),
        ("⏳", "Execution - Step 3", "Correlation analysis"),
        ("❌", "Execution - Step 3", "FAILED: Data incompatibility"),
        ("🚨", "Plan Failure Detection", "Entire plan strategy flawed"),
        ("🤝", "Human Intervention", "Request strategic guidance"),
        ("💡", "Suggestions", "4 alternative strategies provided"),
        ("👤", "Human Decision", "Selected: Simplify & preprocess"),
        ("📋", "New Plan Generated", "5 new steps created"),
        ("🔄", "Recovery", "Discarding old plan, using new one"),
        ("✅", "New Step 1", "Aggregate weather data"),
        ("✅", "New Step 2", "Normalize datasets"),
        ("✅", "New Step 3", "Simplified correlation"),
        ("✅", "New Step 4", "Focus on major events"),
        ("✅", "New Step 5", "Generate report with caveats"),
        ("🎉", "Complete", "Query answered successfully!")
    ]
    
    for i, (status, stage, message) in enumerate(workflow_steps, 1):
        print(f"\n[{i:02d}] {status} {stage}")
        print(f"     └─ {message}")
        await asyncio.sleep(0.6)
    
    # Key Differences
    await asyncio.sleep(2)
    await show_section("PLAN FAILURE vs TOOL FAILURE")
    
    print("🔧 TOOL FAILURE (Previous Demo):")
    print("   • Single tool/API doesn't work")
    print("   • Solution: Use alternative tool")
    print("   • Plan stays the same")
    print("   • Tactical decision")
    
    await asyncio.sleep(2)
    
    print("\n📋 PLAN FAILURE (This Demo):")
    print("   • Entire strategy doesn't work")
    print("   • Solution: Complete plan redesign")
    print("   • Requires strategic rethinking")
    print("   • More complex, happens with complex queries")
    
    await asyncio.sleep(2)
    
    # Statistics
    await show_section("SESSION STATISTICS")
    
    print("📊 Intervention Summary:")
    print(f"   • Intervention Type: PLAN FAILURE")
    print(f"   • Initial Plan Steps: 5")
    print(f"   • Steps Completed Before Failure: 2")
    print(f"   • New Plan Steps: 5")
    print(f"   • New Plan Success Rate: 100%")
    print(f"   • Total Recovery Time: ~15 seconds")
    print(f"   • Final Status: ✅ SUCCESSFUL")
    
    await asyncio.sleep(2)
    
    # Conclusion
    print("\n\n" + "🎬 "*30)
    print("DEMO COMPLETE!".center(180))
    print("🎬 "*30)
    
    print("""
    
    📝 KEY INSIGHTS:
    
    Plan failures are MORE COMMON than tool failures with complex queries because:
    ✅ Complex queries have multi-step dependencies
    ✅ Data format mismatches aren't obvious upfront
    ✅ Initial plans may be too ambitious
    ✅ Assumptions about data compatibility can be wrong
    
    Human-In-Loop is CRITICAL for plan failures because:
    🤝 Humans provide strategic thinking (not just tactical fixes)
    🧠 Humans can simplify scope when needed
    📊 Humans understand acceptable trade-offs
    💡 Humans recognize when to pivot strategy
    
    🚀 This makes the system production-ready for REAL-WORLD complex queries!
    
    📚 Compare with tool failure demo: youtube_demo_automated.py
    
    Thank you for watching! 🙏
    
    """)


if __name__ == "__main__":
    print("\n🎥 Starting Plan Failure demo in 3 seconds...")
    print("📹 Recording tip: This demo shows MORE COMMON failure scenario!\n")
    time.sleep(3)
    
    asyncio.run(main_demo())
