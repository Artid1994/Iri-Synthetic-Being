from __future__ import annotations


class AssociationIndex:
    """ดัชนีความสัมพันธ์ระหว่างประสบการณ์กับสิ่งที่เกี่ยวข้อง"""

    def __init__(self) -> None:
        self._associations: dict[str, list[str]] = {}

    def add(self, experience: str, association: str) -> None:
        values = self._associations.setdefault(experience, [])

        if association not in values:
            values.append(association)

    def find(self, experience: str) -> list[str]:
        experience = experience.strip()

        if not experience:
            return []

        exact = self._associations.get(experience)
        if exact:
            return list(exact)

        words = set(experience.split())

        if "สีโปรด" in experience:
            words.update({"ฉัน", "ชอบ", "สี"})

        matches: list[str] = []

        for stored, associations in self._associations.items():
            if words & set(stored.split()):
                for association in associations:
                    if association not in matches:
                        matches.append(association)

        return matches

    def snapshot(self) -> dict[str, list[str]]:
        return {
            experience: list(associations)
            for experience, associations
            in self._associations.items()
        }
