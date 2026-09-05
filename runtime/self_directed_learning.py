from __future__ import annotations

from runtime.learning_task import LearningTask
from runtime.web_research import WebResearch


class SelfDirectedLearning:
    def __init__(self) -> None:
        self._tasks: list[LearningTask] = []

    def create_task(
        self,
        need: str,
    ) -> LearningTask | None:
        need = need.strip()

        if not need:
            return None

        for task in self._tasks:
            if task.topic == need and task.status in {
                "PENDING",
                "ACTIVE",
            }:
                return None

        task = LearningTask(need)
        self._tasks.append(task)

        return task

    def from_reflection(self, reflection):
        if reflection is None:
            return None

        next_task = getattr(reflection, "next_task", None)

        if not next_task:
            return None

        return self.create_task(next_task)

    def next_task(self) -> LearningTask | None:
        for task in self._tasks:
            if task.status == "PENDING":
                task.start()
                return task

        return None


    def execute_next_search_task(self, memory_graph) -> str:
        """
        ดึงภารกิจที่ค้างอยู่ ส่งไปหาในเน็ต สกัดข้อมูล และแอดเข้า MemoryGraph
        """
        task = self.next_task()
        if not task:
            return "📌 [ระบบ] ไม่มีภารกิจการเรียนรู้ที่ค้างอยู่ในคิว"

        print(f"🌐 [Web Research] กำลังค้นหาข้อมูลสำหรับหัวข้อ: {task.topic}")
        try:
            research_engine = WebResearch()
            # 1. ยิงค้นหาข้อมูลและสกัด HTML ให้สะอาดอัตโนมัติ
            result = research_engine.search(task.topic)

            # 2. นำข้อมูลความรู้ที่ได้ แอดเข้าสู่ MemoryGraph ของสมองเทียม
            node_content = f"Knowledge ({task.topic}): {result.content[:200]}..."
            node_id = memory_graph.add_node(node_content, "WebKnowledge")

            # 3. ปิดภารกิจเมื่อเรียนรู้สำเร็จ
            task.complete()
            print(f"✨ [สำเร็จ] บันทึกความรู้ใหม่เข้าสู่ระบบเรียบร้อย (Node ID: {node_id})")
            return f"✅ สำเร็จ: บันทึกความรู้เรื่อง {task.topic} แล้ว"

        except Exception as e:
            # หากพังหรือติดบล็อก ให้ยกเลิกสถานะเพื่อรอแก้ตัวรอบหน้า
            task.status = "PENDING"
            print(f"❌ [ผิดพลาด] การสืบค้นล้มเหลว: {e}")
            return f"❌ เกิดข้อผิดพลาด: {e}"""
