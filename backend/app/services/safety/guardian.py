from typing import List

FORBIDDEN_KEYWORDS = ["rm -rf", "delete database", "drop table", "system32"]

class SafetyGuardian:
    def check_input(self, text: str) -> bool:
        """
        Check if input contains safe content. Returns True if safe, False if unsafe.
        """
        text_lower = text.lower()
        for keyword in FORBIDDEN_KEYWORDS:
            if keyword in text_lower:
                return False
        return True

    def check_tool_execution(self, tool_name: str, args: dict) -> bool:
        """
        Check if tool execution is safe.
        """
        if tool_name == "code_executor":
            # Strict checks for code execution
            code = args.get("code", "")
            if "os.system" in code or "subprocess" in code:
                return False
        return True

safety_guardian = SafetyGuardian()
