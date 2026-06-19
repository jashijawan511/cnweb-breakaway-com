from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class KeywordNote:
    keyword: str
    note: str
    source_url: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    tags: list = field(default_factory=list)
    priority: int = 5  # 1-10

    def update_note(self, new_note: str) -> None:
        self.note = new_note
        self.updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "note": self.note,
            "source_url": self.source_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "tags": self.tags,
            "priority": self.priority,
        }


@dataclass
class NoteCollection:
    name: str
    notes: list = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for note in self.notes:
            if note.keyword == keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> list:
        return [note for note in self.notes if tag in note.tags]

    def remove_note(self, keyword: str) -> bool:
        note = self.find_by_keyword(keyword)
        if note:
            self.notes.remove(note)
            return True
        return False


def format_note_simple(note: KeywordNote) -> str:
    return f"[{note.keyword}] {note.note[:40]}..."

def format_note_detailed(note: KeywordNote) -> str:
    lines = [
        f"关键字：{note.keyword}",
        f"备注：{note.note}",
        f"来源：{note.source_url}",
        f"创建时间：{note.created_at.strftime('%Y-%m-%d %H:%M')}",
    ]
    if note.updated_at:
        lines.append(f"更新时间：{note.updated_at.strftime('%Y-%m-%d %H:%M')}")
    if note.tags:
        lines.append(f"标签：{'、'.join(note.tags)}")
    lines.append(f"优先级：{note.priority}")
    return "\n".join(lines)

def format_collection_summary(collection: NoteCollection) -> str:
    count = len(collection.notes)
    if count == 0:
        return f"集合「{collection.name}」暂无笔记"
    lines = [f"集合「{collection.name}」共 {count} 条笔记："]
    for i, note in enumerate(collection.notes, 1):
        lines.append(f"  {i}. {format_note_simple(note)}")
    return "\n".join(lines)


if __name__ == "__main__":
    # 示例数据
    note1 = KeywordNote(
        keyword="冰球突破",
        note="冰球突破是一款深受玩家喜爱的在线电子游戏，其核心机制基于经典水果机玩法。",
        source_url="https://cnweb-breakaway.com",
        tags=["游戏", "电子", "经典"],
        priority=8,
    )
    note2 = KeywordNote(
        keyword="冰球突破攻略",
        note="掌握冰球突破的基本规则和高级技巧，有助于提升游戏体验和胜率。",
        source_url="https://cnweb-breakaway.com",
        tags=["攻略", "技巧"],
        priority=6,
    )
    note3 = KeywordNote(
        keyword="冰球突破历史",
        note="了解冰球突破的发展历程和版本变迁，从早期街机到现代在线平台。",
        source_url="https://cnweb-breakaway.com",
        tags=["历史", "发展"],
        priority=4,
    )

    collection = NoteCollection(name="冰球突破笔记")
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    print(format_collection_summary(collection))
    print("\n--- 详细笔记 ---")
    print(format_note_detailed(note1))