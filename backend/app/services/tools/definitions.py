from typing import Any, Type
from pydantic import BaseModel, Field
from duckduckgo_search import DDGS
from app.services.tools.base import Tool
import requests
from bs4 import BeautifulSoup
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None
import docx
import os

class WebSearchInput(BaseModel):
    query: str = Field(description="The query to search for on the web.")

class WebSearchTool(Tool):
    name = "web_search"
    description = "Search the web for information using DuckDuckGo."
    args_schema = WebSearchInput

    def run(self, query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                if not results:
                    return "No results found."
                formatted_results = "\n\n".join(
                    [f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}" for r in results]
                )
                return formatted_results
        except Exception as e:
            return f"Error searching web: {str(e)}"

class CalculatorInput(BaseModel):
    expression: str = Field(description="The mathematical expression to evaluate.")

class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluate a mathematical expression."
    args_schema = CalculatorInput

    def run(self, expression: str) -> str:
        try:
            return str(eval(expression, {"__builtins__": None}, {}))
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"

class WebsiteReaderInput(BaseModel):
    url: str = Field(description="The URL of the website to read.")

class WebsiteReaderTool(Tool):
    name = "website_reader"
    description = "Read the content of a website."
    args_schema = WebsiteReaderInput

    def run(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            
            # Break into lines and remove leading/trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text[:5000] + "..." if len(text) > 5000 else text
        except Exception as e:
            return f"Error reading website: {str(e)}"

class FileReaderInput(BaseModel):
    file_path: str = Field(description="The absolute path to the file to read (txt, pdf, docx).")

class FileReaderTool(Tool):
    name = "file_reader"
    description = "Read the content of a local file."
    args_schema = FileReaderInput

    def run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return "Error: File not found."
            
        try:
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif ext == '.pdf':
                if fitz is None:
                    return "Error: PyMuPDF (fitz) is not installed. PDF reading is unavailable."
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                return text
            elif ext == '.docx':
                doc = docx.Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
            else:
                return f"Error: Unsupported file extension {ext}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

from app.db.base import SessionLocal
from app.db import models
from typing import Optional

class NotesInput(BaseModel):
    action: str = Field(..., description="Action to perform: 'create', 'list', 'read', 'delete'")
    title: Optional[str] = Field(None, description="Title of the note (for create)")
    content: Optional[str] = Field(None, description="Content of the note (for create)")
    note_id: Optional[int] = Field(None, description="ID of the note (for read/delete)")

class NotesTool(Tool):
    name = "notes"
    description = "Manage notes. Actions: create, list, read, delete."
    args_schema = NotesInput

    def run(self, action: str, title: Optional[str] = None, content: Optional[str] = None, note_id: Optional[int] = None) -> str:
        db = SessionLocal()
        try:
            # TODO: How to get current user ID in a tool? 
            # Tools currently don't have context of the user. 
            # We might need to pass user_id to run(), but Base Tool signature is fixed by args_schema.
            # For this "Self-hosted" single user (or simple auth) app, maybe we fetch the first user or pass it in context?
            # Ideally, the `run` method should accept context.
            # Hack for now: Use the first user found or hardcode ID 1 if single user. 
            # Real fix: Tool execution should receive context.
            user = db.query(models.User).first()
            if not user:
                return "Error: No user found."
            user_id = user.id

            if action == 'create':
                note = models.Note(title=title or "Untitled", content=content or "", user_id=user_id)
                db.add(note)
                db.commit()
                return f"Note created with ID: {note.id}"
            
            elif action == 'list':
                notes = db.query(models.Note).filter(models.Note.user_id == user_id).all()
                if not notes:
                    return "No notes found."
                return "\n".join([f"{n.id}: {n.title}" for n in notes])
            
            elif action == 'read':
                if not note_id:
                    return "Error: note_id required for read."
                note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user_id).first()
                if not note:
                    return "Note not found."
                return f"Title: {note.title}\nContent: {note.content}"
            
            elif action == 'delete':
                if not note_id:
                    return "Error: note_id required for delete."
                note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user_id).first()
                if not note:
                    return "Note not found."
                db.delete(note)
                db.commit()
                return "Note deleted."
            
            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"Error managing notes: {str(e)}"
        finally:
            db.close()

class ReminderInput(BaseModel):
    action: str = Field(..., description="Action: 'set', 'list', 'delete'")
    text: Optional[str] = Field(None, description="Reminder text (for set)")
    reminder_id: Optional[int] = Field(None, description="ID of reminder (for delete)")

class ReminderTool(Tool):
    name = "reminder"
    description = "Manage reminders."
    args_schema = ReminderInput

    def run(self, action: str, text: Optional[str] = None, reminder_id: Optional[int] = None) -> str:
        db = SessionLocal()
        try:
            user = db.query(models.User).first()
            if not user:
                return "Error: No user found."
            user_id = user.id

            if action == 'set':
                reminder = models.Reminder(text=text, user_id=user_id)
                db.add(reminder)
                db.commit()
                return f"Reminder set with ID: {reminder.id}"
            
            elif action == 'list':
                reminders = db.query(models.Reminder).filter(models.Reminder.user_id == user_id).all()
                if not reminders:
                    return "No reminders."
                return "\n".join([f"{r.id}: {r.text} (Completed: {r.is_completed})" for r in reminders])
            
            elif action == 'delete':
                if not reminder_id:
                    return "Error: reminder_id required."
                reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id, models.Reminder.user_id == user_id).first()
                if not reminder:
                    return "Reminder not found."
                db.delete(reminder)
                db.commit()
                return "Reminder deleted."
            
            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"Error managing reminders: {str(e)}"
        finally:
            db.close()
