import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
from datetime import datetime
import threading

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:5000"
API_KEY  = "GROUPE10-KEY"
HEADERS  = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PALETTE = {
    "bg":        "#0f1117",
    "surface":   "#1a1d2e",
    "card":      "#21253a",
    "border":    "#2e3250",
    "accent":    "#4f7cff",
    "accent2":   "#a78bfa",
    "success":   "#22c55e",
    "danger":    "#ef4444",
    "warning":   "#f59e0b",
    "text":      "#e2e8f0",
    "muted":     "#64748b",
}

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_LABEL  = ("Segoe UI", 12)
FONT_SMALL  = ("Segoe UI", 10)
FONT_MONO   = ("Consolas", 11)
FONT_BIG    = ("Segoe UI", 32, "bold")


# ─────────────────────────────────────────────
#  API HELPERS
# ─────────────────────────────────────────────
def api_get(path):
    r = requests.get(BASE_URL + path, headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.json()

def api_post(path, data):
    r = requests.post(BASE_URL + path, headers=HEADERS, json=data, timeout=5)
    r.raise_for_status()
    return r.json()

def api_put(path, data):
    r = requests.put(BASE_URL + path, headers=HEADERS, json=data, timeout=5)
    r.raise_for_status()
    return r.json()

def api_delete(path):
    r = requests.delete(BASE_URL + path, headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.status_code


# ─────────────────────────────────────────────
#  TOAST NOTIFICATION
# ─────────────────────────────────────────────
class Toast(ctk.CTkToplevel):
    def __init__(self, master, message, kind="success"):
        super().__init__(master)
        color = PALETTE["success"] if kind == "success" else PALETTE["danger"] if kind == "error" else PALETTE["warning"]
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=color)
        self.resizable(False, False)

        ctk.CTkLabel(self, text=message, font=FONT_LABEL,
                     text_color="white", fg_color=color).pack(padx=20, pady=12)

        # Position bottom-right of screen
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        self.geometry(f"+{sw - w - 30}+{sh - h - 70}")
        self.after(2500, self.destroy)


def toast(master, msg, kind="success"):
    try:
        Toast(master, msg, kind)
    except Exception:
        pass


# ─────────────────────────────────────────────
#  MODAL DIALOG BASE
# ─────────────────────────────────────────────
class ModalDialog(ctk.CTkToplevel):
    def __init__(self, master, title, width=480, height=380):
        super().__init__(master)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.configure(fg_color=PALETTE["surface"])
        self.grab_set()
        self.focus()
        self.result = None

        header = ctk.CTkFrame(self, fg_color=PALETTE["card"], corner_radius=0, height=52)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=title, font=FONT_TITLE,
                     text_color=PALETTE["accent"]).pack(side="left", padx=20, pady=12)

        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=24, pady=16)


# ─────────────────────────────────────────────
#  DIALOG: AJOUTER / MODIFIER ÉTUDIANT
# ─────────────────────────────────────────────
class StudentDialog(ModalDialog):
    def __init__(self, master, student=None, subjects=None, initial_grades=None):
        mode = "Modifier l'Étudiant" if student else "Nouvel Étudiant"
        self.subjects = subjects or []
        self.initial_grades = initial_grades or [] # List of grade dicts
        
        # Increase height for the integrated grade list
        super().__init__(master, mode, width=540, height=580)
        self.student = student

        # Profile Section
        profile = ctk.CTkFrame(self.body, fg_color="transparent")
        profile.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(profile, text="Matricule", font=FONT_SMALL,
                     text_color=PALETTE["muted"]).grid(row=0, column=0, sticky="w", padx=(0,10))
        self.ent_id = ctk.CTkEntry(profile, placeholder_text="ex: MAT-001", width=160,
                                   fg_color=PALETTE["card"], border_color=PALETTE["border"])
        self.ent_id.grid(row=1, column=0, sticky="w", padx=(0,10), pady=(2, 10))

        ctk.CTkLabel(profile, text="Nom Complet", font=FONT_SMALL,
                     text_color=PALETTE["muted"]).grid(row=0, column=1, sticky="w")
        self.ent_name = ctk.CTkEntry(profile, placeholder_text="Prénom NOM", width=280,
                                     fg_color=PALETTE["card"], border_color=PALETTE["border"])
        self.ent_name.grid(row=1, column=1, sticky="w", pady=(2, 10))

        if student:
            self.ent_id.insert(0, student.get("id", ""))
            self.ent_name.insert(0, student.get("name", ""))
            self.ent_id.configure(state="disabled") # Matricule non modifiable

        # Grades Section
        ctk.CTkLabel(self.body, text="Résultats par Matière (CC & Examen)", font=("Segoe UI", 13, "bold"),
                     text_color=PALETTE["accent"]).pack(anchor="w", pady=(10, 5))
        
        # Table Header
        h_frame = ctk.CTkFrame(self.body, fg_color=PALETTE["border"], height=30, corner_radius=6)
        h_frame.pack(fill="x", pady=2)
        h_frame.pack_propagate(False)
        ctk.CTkLabel(h_frame, text="Matière", font=FONT_SMALL, width=220, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(h_frame, text="CC", font=FONT_SMALL, width=80).pack(side="left")
        ctk.CTkLabel(h_frame, text="Exam", font=FONT_SMALL, width=80).pack(side="left")

        self.scroll_grades = ctk.CTkScrollableFrame(self.body, fg_color=PALETTE["card"], height=240, corner_radius=10)
        self.scroll_grades.pack(fill="both", expand=True, pady=(5, 15))

        self.grade_entries = {} # {subj_id: (cc_ent, exam_ent, original_grade_obj)}
        for s in self.subjects:
            row = ctk.CTkFrame(self.scroll_grades, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=s.get("name", s.get("id")), font=FONT_LABEL, width=220, anchor="w",
                         text_color=PALETTE["text"]).pack(side="left", padx=5)
            
            cc_ent = ctk.CTkEntry(row, width=70, fg_color=PALETTE["surface"], border_width=1)
            cc_ent.pack(side="left", padx=5)
            
            ex_ent = ctk.CTkEntry(row, width=70, fg_color=PALETTE["surface"], border_width=1)
            ex_ent.pack(side="left", padx=5)
            
            # Find existing grade
            orig = None
            for g in self.initial_grades:
                if g.get("subject_id") == s.get("id"):
                    cc_ent.insert(0, str(g.get("cc", "")))
                    ex_ent.insert(0, str(g.get("exam", "")))
                    orig = g
                    break
            
            self.grade_entries[s['id']] = (cc_ent, ex_ent, orig)

        btn_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        btn_frame.pack(fill="x")
        ctk.CTkButton(btn_frame, text="Annuler", fg_color=PALETTE["card"],
                      hover_color=PALETTE["border"], command=self.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_frame, text="Tout Enregistrer", fg_color=PALETTE["accent"],
                      command=self._save).pack(side="right")

    def _save(self):
        sid  = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        if not sid or not name:
            toast(self, "Tous les champs profil sont requis", "error")
            return
        
        # Collect results
        grade_results = []
        for s_id, (cc_ent, ex_ent, orig) in self.grade_entries.items():
            cc_val = cc_ent.get().strip()
            ex_val = ex_ent.get().strip()
            
            if not cc_val and not ex_val: continue # Skip empty
            
            try:
                cc = float(cc_val)
                ex = float(ex_val)
                assert 0 <= cc <= 20 and 0 <= ex <= 20
                grade_results.append({
                    "id": orig['id'] if orig else None,
                    "subject_id": s_id,
                    "cc": cc,
                    "exam": ex
                })
            except Exception:
                toast(self, f"Note invalide pour une matière", "error")
                return

        self.result = {
            "student": {"id": sid, "name": name},
            "grades": grade_results
        }
        self.destroy()


# ─────────────────────────────────────────────
#  DIALOG: AJOUTER NOTE
# ─────────────────────────────────────────────
class GradeDialog(ModalDialog):
    def __init__(self, master, student_id, subjects, grade_obj=None):
        title = f"Modifier Résultat" if grade_obj else f"Saisir un Résultat"
        super().__init__(master, f"{title} — {student_id}", width=440, height=380)
        self.student_id = student_id
        self.subjects = subjects
        self.grade_obj = grade_obj

        ctk.CTkLabel(self.body, text="Matière", font=FONT_SMALL,
                     text_color=PALETTE["muted"]).pack(anchor="w")
        self.combo_subject = ctk.CTkComboBox(self.body,
                                             values=[s.get("name", s.get("id", "")) for s in subjects],
                                             fg_color=PALETTE["card"], border_color=PALETTE["border"])
        self.combo_subject.pack(fill="x", pady=(2, 12))

        # CC Entry
        ctk.CTkLabel(self.body, text="Contrôle Continu (CC)", font=FONT_SMALL,
                     text_color=PALETTE["muted"]).pack(anchor="w")
        self.ent_cc = ctk.CTkEntry(self.body, placeholder_text="ex: 14",
                                   fg_color=PALETTE["card"], border_color=PALETTE["border"])
        self.ent_cc.pack(fill="x", pady=(2, 12))

        # Exam Entry
        ctk.CTkLabel(self.body, text="Examen (EX)", font=FONT_SMALL,
                     text_color=PALETTE["muted"]).pack(anchor="w")
        self.ent_exam = ctk.CTkEntry(self.body, placeholder_text="ex: 15.5",
                                     fg_color=PALETTE["card"], border_color=PALETTE["border"])
        self.ent_exam.pack(fill="x", pady=(2, 20))

        if grade_obj:
            # find subject name
            full_name = grade_obj.get("subject_id")
            for s in subjects:
                if s.get("id") == grade_obj.get("subject_id"):
                    full_name = s.get("name")
                    break
            self.combo_subject.set(full_name)
            self.ent_cc.insert(0, str(grade_obj.get("cc", "")))
            self.ent_exam.insert(0, str(grade_obj.get("exam", "")))

        btn_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        btn_frame.pack(fill="x")
        ctk.CTkButton(btn_frame, text="Annuler", fg_color=PALETTE["card"],
                      hover_color=PALETTE["border"], command=self.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_frame, text="Enregistrer", fg_color=PALETTE["accent"],
                      command=self._save).pack(side="right")

    def _save(self):
        subj_name = self.combo_subject.get().strip()
        cc_val    = self.ent_cc.get().strip()
        ex_val    = self.ent_exam.get().strip()

        subj_id = None
        for s in self.subjects:
            if s.get("name", s.get("id", "")) == subj_name:
                subj_id = s.get("id", subj_name)
                break
        if not subj_id: subj_id = subj_name

        try:
            cc = float(cc_val)
            ex = float(ex_val)
            assert 0 <= cc <= 20 and 0 <= ex <= 20
        except Exception:
            toast(self, "Valeurs invalides (0-20)", "error")
            return
            
        self.result = {
            "student_id": self.student_id,
            "subject_id": subj_id,
            "cc": cc,
            "exam": ex
        }
        self.destroy()


# ─────────────────────────────────────────────
#  DIALOG: AJOUTER / MODIFIER MATIÈRE
# ─────────────────────────────────────────────
class SubjectDialog(ModalDialog):
    def __init__(self, master, subject=None):
        mode = "Modifier la Matière" if subject else "Nouvelle Matière"
        super().__init__(master, mode, width=440, height=260)
        self.subject = subject

        ctk.CTkLabel(self.body, text="ID / Code Matière", font=FONT_SMALL,
                     text_color=PALETTE["muted"]).pack(anchor="w")
        self.ent_id = ctk.CTkEntry(self.body, placeholder_text="ex: MATH101",
                                   fg_color=PALETTE["card"], border_color=PALETTE["border"])
        self.ent_id.pack(fill="x", pady=(2, 12))

        ctk.CTkLabel(self.body, text="Intitulé de la Matière", font=FONT_SMALL,
                     text_color=PALETTE["muted"]).pack(anchor="w")
        self.ent_name = ctk.CTkEntry(self.body, placeholder_text="ex: Mathématiques",
                                     fg_color=PALETTE["card"], border_color=PALETTE["border"])
        self.ent_name.pack(fill="x", pady=(2, 12))

        ctk.CTkLabel(self.body, text="Crédits (ECTS)", font=FONT_SMALL,
                     text_color=PALETTE["muted"]).pack(anchor="w")
        self.ent_credits = ctk.CTkEntry(self.body, placeholder_text="ex: 6",
                                         fg_color=PALETTE["card"], border_color=PALETTE["border"])
        self.ent_credits.pack(fill="x", pady=(2, 20))

        if subject:
            self.ent_id.insert(0, subject.get("id", ""))
            self.ent_name.insert(0, subject.get("name", ""))
            self.ent_credits.insert(0, str(subject.get("credits", "0")))

        btn_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        btn_frame.pack(fill="x")
        ctk.CTkButton(btn_frame, text="Annuler", fg_color=PALETTE["card"],
                      hover_color=PALETTE["border"], command=self.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_frame, text="Enregistrer", fg_color=PALETTE["accent"],
                      command=self._save).pack(side="right")

    def _save(self):
        sid  = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        cred = self.ent_credits.get().strip()
        if not sid or not name:
            toast(self, "ID et Nom sont requis", "error")
            return
        try:
            val_cred = int(cred)
        except Exception:
            val_cred = 0
        self.result = {"id": sid, "name": name, "credits": val_cred}
        self.destroy()


# ─────────────────────────────────────────────
#  PAGE: DASHBOARD
# ─────────────────────────────────────────────
class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        # Title row
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(hdr, text="Dashboard", font=FONT_TITLE,
                     text_color=PALETTE["text"]).pack(side="left")
        ctk.CTkLabel(hdr, text=datetime.now().strftime("%d %B %Y"),
                     font=FONT_SMALL, text_color=PALETTE["muted"]).pack(side="right", padx=4)

        # KPI cards row
        self.kpi_row = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_row.pack(fill="x", pady=(0, 20))
        self.kpi_row.columnconfigure((0, 1, 2, 3), weight=1, uniform="kpi")

        self.kpi_cards = {}
        kpis = [
            ("Étudiants",  "👤", PALETTE["accent"]),
            ("Matières",   "📚", PALETTE["accent2"]),
            ("Résultats",  "📝", PALETTE["success"]),
            ("Moy. Géné.", "📊", PALETTE["warning"]),
        ]
        for i, (label, icon, color) in enumerate(kpis):
            card = ctk.CTkFrame(self.kpi_row, fg_color=PALETTE["card"],
                                corner_radius=14, border_width=1, border_color=PALETTE["border"])
            card.grid(row=0, column=i, padx=8, sticky="ew")
            ctk.CTkLabel(card, text=icon, font=("Segoe UI Emoji", 26)).pack(pady=(16, 0))
            val_lbl = ctk.CTkLabel(card, text="—", font=FONT_BIG, text_color=color)
            val_lbl.pack()
            ctk.CTkLabel(card, text=label, font=FONT_SMALL,
                         text_color=PALETTE["muted"]).pack(pady=(0, 16))
            self.kpi_cards[label] = val_lbl

        # Recent activity
        ctk.CTkLabel(self, text="Aperçu des Étudiants", font=("Segoe UI", 13, "bold"),
                     text_color=PALETTE["muted"]).pack(anchor="w", pady=(0, 8))
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=PALETTE["card"],
                                              corner_radius=12, height=260)
        self.scroll.pack(fill="both", expand=True)

    def refresh(self):
        try:
            students = api_get("/students")
            subjects = api_get("/subjects") if _endpoint_exists("/subjects") else []
            grades   = []
            for s in students:
                try:
                    g = api_get(f"/students/{s['id']}/grades")
                    grades.extend(g if isinstance(g, list) else [])
                except Exception:
                    pass

            self.kpi_cards["Étudiants"].configure(text=str(len(students)))
            self.kpi_cards["Matières"].configure(text=str(len(subjects)))
            self.kpi_cards["Résultats"].configure(text=str(len(grades)))

            all_vals = [g.get("grade", g.get("value", 0)) for g in grades if isinstance(g, dict)]
            avg = (sum(all_vals) / len(all_vals)) if all_vals else 0
            color = PALETTE["success"] if avg >= 10 else PALETTE["danger"]
            self.kpi_cards["Moy. Géné."].configure(text=f"{avg:.1f}", text_color=color)

            # Populate list
            for w in self.scroll.winfo_children():
                w.destroy()
            for stu in students:
                row = ctk.CTkFrame(self.scroll, fg_color=PALETTE["surface"], corner_radius=8)
                row.pack(fill="x", pady=3, padx=4)
                ctk.CTkLabel(row, text=f"  {stu.get('id', '?')}",
                             font=FONT_MONO, text_color=PALETTE["accent"], width=120).pack(side="left")
                ctk.CTkLabel(row, text=stu.get("name", "—"),
                             font=FONT_LABEL, text_color=PALETTE["text"]).pack(side="left", padx=8)

                # student avg
                stu_grades = [g.get("grade", g.get("value", 0))
                              for g in grades
                              if g.get("student_id") == stu.get("id")]
                if stu_grades:
                    avg_s = sum(stu_grades) / len(stu_grades)
                    c = PALETTE["success"] if avg_s >= 10 else PALETTE["danger"]
                    ctk.CTkLabel(row, text=f"Moy: {avg_s:.1f}/20",
                                 font=FONT_SMALL, text_color=c).pack(side="right", padx=12)

        except requests.exceptions.ConnectionError:
            self.kpi_cards["Étudiants"].configure(text="⚠")
            self.kpi_cards["Matières"].configure(text="⚠")
            self.kpi_cards["Notes"].configure(text="⚠")
            self.kpi_cards["Moy. Géné."].configure(text="⚠")


def _endpoint_exists(path):
    try:
        api_get(path)
        return True
    except Exception:
        return False


# ─────────────────────────────────────────────
#  PAGE: ÉTUDIANTS
# ─────────────────────────────────────────────
class StudentsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(toolbar, text="Gestion des Étudiants",
                     font=FONT_TITLE, text_color=PALETTE["text"]).pack(side="left")

        ctk.CTkButton(toolbar, text="+ Ajouter", fg_color=PALETTE["accent"],
                      command=self._add, width=110).pack(side="right", padx=4)
        ctk.CTkButton(toolbar, text="⟳ Rafraîchir", fg_color=PALETTE["card"],
                      hover_color=PALETTE["border"], command=self.refresh, width=110).pack(side="right", padx=4)

        # Search bar
        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.pack(fill="x", pady=(0, 10))
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter())
        ctk.CTkEntry(search_row, textvariable=self.search_var,
                     placeholder_text="🔍  Rechercher un étudiant…",
                     fg_color=PALETTE["card"], border_color=PALETTE["border"],
                     height=36).pack(fill="x")

        # Table header
        hdr = ctk.CTkFrame(self, fg_color=PALETTE["border"], corner_radius=8, height=36)
        hdr.pack(fill="x", pady=(0, 4))
        hdr.pack_propagate(False)
        for col, w in [("Matricule", 140), ("Nom Complet", 300), ("Moy.", 80), ("Actions", 200)]:
            ctk.CTkLabel(hdr, text=col, font=("Segoe UI", 11, "bold"),
                         text_color=PALETTE["muted"], width=w).pack(side="left", padx=6)

        # Scrollable list
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=PALETTE["card"],
                                              corner_radius=12)
        self.scroll.pack(fill="both", expand=True)

        self._students = []
        self.refresh()

    def refresh(self):
        try:
            self._students = api_get("/students")
        except Exception:
            self._students = []
        self._filter()

    def _filter(self):
        query = self.search_var.get().lower()
        filtered = [s for s in self._students
                    if query in s.get("id", "").lower() or query in s.get("name", "").lower()]
        self._render(filtered)

    def _render(self, students):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not students:
            ctk.CTkLabel(self.scroll, text="Aucun étudiant trouvé.",
                         text_color=PALETTE["muted"], font=FONT_LABEL).pack(pady=40)
            return

        for stu in students:
            row = ctk.CTkFrame(self.scroll, fg_color=PALETTE["surface"], corner_radius=8)
            row.pack(fill="x", pady=3, padx=2)

            ctk.CTkLabel(row, text=stu.get("id", "?"), font=FONT_MONO,
                         text_color=PALETTE["accent"], width=140).pack(side="left", padx=6)
            ctk.CTkLabel(row, text=stu.get("name", "—"), font=FONT_LABEL,
                         text_color=PALETTE["text"], width=300).pack(side="left")

            # Fetch avg lazily (simple sync here; production would use threads)
            try:
                grades = api_get(f"/students/{stu['id']}/grades")
                vals   = [g.get("grade", g.get("value", 0)) for g in grades if isinstance(g, dict)]
                avg    = sum(vals) / len(vals) if vals else None
                color  = PALETTE["success"] if avg and avg >= 10 else PALETTE["danger"] if avg else PALETTE["muted"]
                avg_txt = f"{avg:.1f}" if avg is not None else "—"
            except Exception:
                avg_txt, color = "—", PALETTE["muted"]

            ctk.CTkLabel(row, text=avg_txt, font=("Segoe UI", 12, "bold"),
                         text_color=color, width=80).pack(side="left")

            # Action buttons
            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.pack(side="right", padx=8, pady=4)

            ctk.CTkButton(actions, text="Notes", width=70, height=26,
                          fg_color=PALETTE["accent2"], hover_color="#7c3aed",
                          font=FONT_SMALL,
                          command=lambda s=stu: self._open_grades(s)).pack(side="left", padx=3)
            ctk.CTkButton(actions, text="Modifier", width=70, height=26,
                          fg_color=PALETTE["card"], hover_color=PALETTE["border"],
                          font=FONT_SMALL,
                          command=lambda s=stu: self._edit(s)).pack(side="left", padx=3)
            ctk.CTkButton(actions, text="Supprimer", width=80, height=26,
                          fg_color=PALETTE["danger"], hover_color="#b91c1c",
                          font=FONT_SMALL,
                          command=lambda s=stu: self._delete(s)).pack(side="left", padx=3)

    def _add(self):
        try:
            subjects = api_get("/subjects")
        except Exception:
            subjects = []
            
        dlg = StudentDialog(self, subjects=subjects)
        self.wait_window(dlg)
        if dlg.result:
            try:
                # 1. Save Profile
                api_post("/students", dlg.result["student"])
                
                # 2. Save Grades
                for g in dlg.result["grades"]:
                    g["student_id"] = dlg.result["student"]["id"]
                    api_post("/grades", g)
                    
                toast(self, f"Étudiant {dlg.result['student']['id']} créé ✓")
                self.refresh()
            except Exception as e:
                toast(self, f"Erreur : {e}", "error")

    def _edit(self, stu):
        try:
            subjects = api_get("/subjects")
            grades   = api_get(f"/students/{stu['id']}/grades")
        except Exception:
            subjects, grades = [], []
            
        dlg = StudentDialog(self, student=stu, subjects=subjects, initial_grades=grades)
        self.wait_window(dlg)
        if dlg.result:
            try:
                # 1. Update Profile
                api_put(f"/students/{stu['id']}", dlg.result["student"])
                
                # 2. Update / Create Grades
                for g in dlg.result["grades"]:
                    g["student_id"] = stu['id']
                    if g.get("id"):
                        api_put(f"/grades/{g['id']}", g)
                    else:
                        api_post("/grades", g)
                        
                toast(self, "Profil et résultats mis à jour ✓")
                self.refresh()
            except Exception as e:
                toast(self, f"Erreur : {e}", "error")

    def _delete(self, stu):
        if not messagebox.askyesno("Confirmer", f"Supprimer {stu.get('name')} ?"):
            return
        try:
            api_delete(f"/students/{stu['id']}")
            toast(self, "Étudiant supprimé")
            self.refresh()
        except Exception as e:
            toast(self, f"Erreur : {e}", "error")

    def _open_grades(self, stu):
        try:
            subjects = api_get("/subjects")
        except Exception:
            subjects = []
        GradesWindow(self, stu, subjects)


# ─────────────────────────────────────────────
#  FENÊTRE NOTES D'UN ÉTUDIANT
# ─────────────────────────────────────────────
class GradesWindow(ctk.CTkToplevel):
    def __init__(self, master, student, subjects):
        super().__init__(master)
        self.student  = student
        self.subjects = subjects
        self.title(f"Notes — {student.get('name', student.get('id'))}")
        self.geometry("600x480")
        self.configure(fg_color=PALETTE["surface"])
        self.grab_set()
        self.focus()

        hdr = ctk.CTkFrame(self, fg_color=PALETTE["card"], corner_radius=0, height=52)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=f"📝  Notes de {student.get('name', '?')}",
                     font=FONT_TITLE, text_color=PALETTE["accent"]).pack(side="left", padx=20, pady=10)

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(toolbar, text="+ Ajouter une Note", fg_color=PALETTE["accent"],
                      command=self._add_grade).pack(side="left")
        ctk.CTkButton(toolbar, text="⟳ Rafraîchir", fg_color=PALETTE["card"],
                      hover_color=PALETTE["border"], command=self.refresh).pack(side="left", padx=8)

        # Table header
        cols_hdr = ctk.CTkFrame(self, fg_color=PALETTE["border"], corner_radius=6, height=32)
        cols_hdr.pack(fill="x", padx=20, pady=(0, 4))
        cols_hdr.pack_propagate(False)
        # Matière, CC, Exam, Total, Actions
        for col, w in [("Matière", 180), ("CC", 60), ("Exam", 60), ("Total", 80), ("Crédits", 60), ("Action", 100)]:
            ctk.CTkLabel(cols_hdr, text=col, font=("Segoe UI", 10, "bold"),
                         text_color=PALETTE["muted"], width=w).pack(side="left", padx=6)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=PALETTE["card"],
                                              corner_radius=10)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        self.refresh()

    def refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        try:
            grades = api_get(f"/students/{self.student['id']}/grades")
            if not grades:
                ctk.CTkLabel(self.scroll, text="Aucune note enregistrée.",
                             text_color=PALETTE["muted"]).pack(pady=30)
                return

            for g in grades:
                subj_id = g.get("subject_id", "?")
                cc      = g.get("cc", 0)
                exam    = g.get("exam", 0)
                total   = g.get("grade", 0)
                grade_id = g.get("id", None)
                
                # find subject credits
                credits = "?"
                subj_name = subj_id
                for s in self.subjects:
                    if s.get("id") == subj_id:
                        credits = str(s.get("credits", "0"))
                        subj_name = s.get("name")
                        break

                mention, color = self._mention(total)

                row = ctk.CTkFrame(self.scroll, fg_color=PALETTE["surface"], corner_radius=6)
                row.pack(fill="x", pady=2, padx=2)

                ctk.CTkLabel(row, text=str(subj_name), font=FONT_LABEL,
                             text_color=PALETTE["text"], width=180, anchor="w").pack(side="left", padx=6)
                ctk.CTkLabel(row, text=str(cc), font=FONT_SMALL,
                             text_color=PALETTE["muted"], width=60).pack(side="left")
                ctk.CTkLabel(row, text=str(exam), font=FONT_SMALL,
                             text_color=PALETTE["muted"], width=60).pack(side="left")
                ctk.CTkLabel(row, text=str(total), font=("Segoe UI", 13, "bold"),
                             text_color=color, width=80).pack(side="left")
                ctk.CTkLabel(row, text=credits, font=FONT_SMALL,
                             text_color=PALETTE["accent2"], width=60).pack(side="left")

                actions = ctk.CTkFrame(row, fg_color="transparent")
                actions.pack(side="right", padx=6)

                ctk.CTkButton(actions, text="✎", width=32, height=26,
                                fg_color=PALETTE["card"], hover_color=PALETTE["border"],
                                font=FONT_SMALL,
                                command=lambda obj=g: self._edit_grade(obj)).pack(side="left", padx=2)

                if grade_id:
                    ctk.CTkButton(actions, text="✕", width=32, height=26,
                                  fg_color=PALETTE["danger"], hover_color="#b91c1c",
                                  font=FONT_SMALL,
                                  command=lambda gid=grade_id: self._delete_grade(gid)).pack(side="left", padx=2)

        except Exception as e:
            ctk.CTkLabel(self.scroll, text=f"Erreur: {e}",
                         text_color=PALETTE["danger"]).pack(pady=30)

    def _mention(self, val):
        try:
            v = float(val)
            if v >= 16:   return "Très Bien",  PALETTE["success"]
            if v >= 14:   return "Bien",        PALETTE["success"]
            if v >= 12:   return "Assez Bien",  PALETTE["warning"]
            if v >= 10:   return "Passable",    PALETTE["warning"]
            return "Insuffisant", PALETTE["danger"]
        except Exception:
            return "—", PALETTE["muted"]

    def _add_grade(self):
        if not self.subjects:
            toast(self, "Aucune matière disponible", "warning")
            return
        dlg = GradeDialog(self, self.student["id"], self.subjects)
        self.wait_window(dlg)
        if dlg.result:
            try:
                api_post(f"/students/{self.student['id']}/grades", dlg.result)
                toast(self, "Résultat enregistré ✓")
                self.refresh()
            except Exception as e:
                toast(self, f"Erreur : {e}", "error")

    def _edit_grade(self, grade_obj):
        dlg = GradeDialog(self, self.student["id"], self.subjects, grade_obj=grade_obj)
        self.wait_window(dlg)
        if dlg.result:
            try:
                api_put(f"/grades/{grade_obj['id']}", dlg.result)
                toast(self, "Résultat mis à jour ✓")
                self.refresh()
            except Exception as e:
                toast(self, f"Erreur : {e}", "error")

    def _delete_grade(self, grade_id):
        if not messagebox.askyesno("Confirmer", "Supprimer cette note ?"):
            return
        try:
            api_delete(f"/grades/{grade_id}")
            toast(self, "Note supprimée")
            self.refresh()
        except Exception as e:
            toast(self, f"Erreur : {e}", "error")


# ─────────────────────────────────────────────
#  PAGE: MATIÈRES
# ─────────────────────────────────────────────
class SubjectsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(toolbar, text="Gestion des Matières",
                     font=FONT_TITLE, text_color=PALETTE["text"]).pack(side="left")
        ctk.CTkButton(toolbar, text="+ Ajouter", fg_color=PALETTE["accent"],
                      command=self._add, width=110).pack(side="right", padx=4)
        ctk.CTkButton(toolbar, text="⟳ Rafraîchir", fg_color=PALETTE["card"],
                      hover_color=PALETTE["border"], command=self.refresh, width=110).pack(side="right", padx=4)

        hdr = ctk.CTkFrame(self, fg_color=PALETTE["border"], corner_radius=8, height=36)
        hdr.pack(fill="x", pady=(0, 4))
        hdr.pack_propagate(False)
        for col, w in [("Code", 120), ("Intitulé", 320), ("Crédits", 80), ("Actions", 180)]:
            ctk.CTkLabel(hdr, text=col, font=("Segoe UI", 11, "bold"),
                         text_color=PALETTE["muted"], width=w).pack(side="left", padx=6)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=PALETTE["card"], corner_radius=12)
        self.scroll.pack(fill="both", expand=True)

        self._subjects = []
        self.refresh()

    def refresh(self):
        try:
            self._subjects = api_get("/subjects")
        except Exception:
            self._subjects = []
        self._render()

    def _render(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        if not self._subjects:
            ctk.CTkLabel(self.scroll, text="Aucune matière enregistrée.",
                         text_color=PALETTE["muted"]).pack(pady=40)
            return
        for subj in self._subjects:
            row = ctk.CTkFrame(self.scroll, fg_color=PALETTE["surface"], corner_radius=8)
            row.pack(fill="x", pady=3, padx=2)
            ctk.CTkLabel(row, text=subj.get("id", "?"), font=FONT_MONO,
                         text_color=PALETTE["accent2"], width=120).pack(side="left", padx=6)
            ctk.CTkLabel(row, text=subj.get("name", "—"), font=FONT_LABEL,
                         text_color=PALETTE["text"], width=320).pack(side="left")
            ctk.CTkLabel(row, text=str(subj.get("credits", "0")), font=FONT_LABEL,
                         text_color=PALETTE["muted"], width=80).pack(side="left")

            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.pack(side="right", padx=8, pady=4)
            ctk.CTkButton(actions, text="Modifier", width=80, height=26,
                          fg_color=PALETTE["card"], hover_color=PALETTE["border"],
                          font=FONT_SMALL,
                          command=lambda s=subj: self._edit(s)).pack(side="left", padx=3)
            ctk.CTkButton(actions, text="Supprimer", width=90, height=26,
                          fg_color=PALETTE["danger"], hover_color="#b91c1c",
                          font=FONT_SMALL,
                          command=lambda s=subj: self._delete(s)).pack(side="left", padx=3)

    def _add(self):
        dlg = SubjectDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            try:
                api_post("/subjects", dlg.result)
                toast(self, "Matière ajoutée ✓")
                self.refresh()
            except Exception as e:
                toast(self, f"Erreur : {e}", "error")

    def _edit(self, subj):
        dlg = SubjectDialog(self, subject=subj)
        self.wait_window(dlg)
        if dlg.result:
            try:
                api_put(f"/subjects/{subj['id']}", dlg.result)
                toast(self, "Matière mise à jour ✓")
                self.refresh()
            except Exception as e:
                toast(self, f"Erreur : {e}", "error")

    def _delete(self, subj):
        if not messagebox.askyesno("Confirmer", f"Supprimer {subj.get('name')} ?"):
            return
        try:
            api_delete(f"/subjects/{subj['id']}")
            toast(self, "Matière supprimée")
            self.refresh()
        except Exception as e:
            toast(self, f"Erreur : {e}", "error")


# ─────────────────────────────────────────────
#  PAGE: STATISTIQUES
# ─────────────────────────────────────────────
class StatsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Statistiques & Classement",
                     font=FONT_TITLE, text_color=PALETTE["text"]).pack(anchor="w", pady=(0, 16))

        ctk.CTkButton(self, text="⟳ Calculer les Stats", fg_color=PALETTE["accent"],
                      command=self.refresh).pack(anchor="w", pady=(0, 16))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=PALETTE["card"], corner_radius=12)
        self.scroll.pack(fill="both", expand=True)

    def refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        try:
            students = api_get("/students")
            subjects = api_get("/subjects")
            data = []
            for stu in students:
                try:
                    grades = api_get(f"/students/{stu['id']}/grades")
                    vals   = [float(g.get("grade", g.get("value", 0))) for g in grades if isinstance(g, dict)]
                    avg    = round(sum(vals) / len(vals), 2) if vals else 0
                    
                    # Calul des crédits validés
                    valid_credits = 0
                    for g in grades:
                        if float(g.get("grade", 0)) >= 10:
                            # find subject credits
                            for s in subjects:
                                if s.get("id") == g.get("subject_id"):
                                    valid_credits += s.get("credits", 0)
                                    break
                                    
                    data.append({**stu, "avg": avg, "count": len(vals), "credits": valid_credits})
                except Exception:
                    data.append({**stu, "avg": 0, "count": 0, "credits": 0})

            data.sort(key=lambda x: x["avg"], reverse=True)

            # Header
            hdr = ctk.CTkFrame(self.scroll, fg_color=PALETTE["border"], corner_radius=6, height=32)
            hdr.pack(fill="x", pady=(0, 4), padx=2)
            hdr.pack_propagate(False)
            for col, w in [("Rang", 60), ("Matricule", 130), ("Nom", 230), ("Moy.", 80), ("Crédits", 100), ("Mention", 150)]:
                ctk.CTkLabel(hdr, text=col, font=("Segoe UI", 10, "bold"),
                             text_color=PALETTE["muted"], width=w).pack(side="left", padx=4)

            medals = {0: "🥇", 1: "🥈", 2: "🥉"}
            for i, stu in enumerate(data):
                row = ctk.CTkFrame(self.scroll, fg_color=PALETTE["surface"], corner_radius=6)
                row.pack(fill="x", pady=2, padx=2)

                rank_txt = medals.get(i, f"#{i+1}")
                ctk.CTkLabel(row, text=rank_txt, width=60).pack(side="left", padx=4)
                ctk.CTkLabel(row, text=stu.get("id", "?"), font=FONT_MONO,
                             text_color=PALETTE["accent"], width=130).pack(side="left")
                ctk.CTkLabel(row, text=stu.get("name", "—"), font=FONT_LABEL,
                             text_color=PALETTE["text"], width=260).pack(side="left")

                avg = stu["avg"]
                color = PALETTE["success"] if avg >= 10 else PALETTE["danger"]
                ctk.CTkLabel(row, text=f"{avg:.2f}", font=("Segoe UI", 13, "bold"),
                             text_color=color, width=80).pack(side="left")
                ctk.CTkLabel(row, text=f"{stu['credits']} ECTS", font=FONT_SMALL,
                             text_color=PALETTE["accent2"], width=100).pack(side="left")

                mention = self._mention(avg)
                ctk.CTkLabel(row, text=mention, font=FONT_SMALL,
                             text_color=color, width=150).pack(side="left")

        except requests.exceptions.ConnectionError:
            ctk.CTkLabel(self.scroll, text="⚠ Serveur inaccessible",
                         text_color=PALETTE["danger"], font=FONT_LABEL).pack(pady=40)

    def _mention(self, avg):
        if avg >= 16: return "Très Bien"
        if avg >= 14: return "Bien"
        if avg >= 12: return "Assez Bien"
        if avg >= 10: return "Passable"
        return "Insuffisant"


# ─────────────────────────────────────────────
#  MAIN APPLICATION WINDOW
# ─────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Keyce Grading Pro — Groupe 10")
        self.geometry("1100x700")
        self.minsize(900, 580)
        self.configure(fg_color=PALETTE["bg"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()
        self._select("dashboard")

    # ── Sidebar ──────────────────────────────
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=PALETTE["surface"],
                               corner_radius=0, width=210)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Logo area
        logo_frame = ctk.CTkFrame(sidebar, fg_color=PALETTE["card"],
                                  corner_radius=0, height=64)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        ctk.CTkLabel(logo_frame, text="🎓  Keyce Grading",
                     font=("Segoe UI", 15, "bold"),
                     text_color=PALETTE["accent"]).pack(padx=16, pady=18, anchor="w")

        # Server status
        self.status_dot = ctk.CTkLabel(sidebar, text="●  Connexion…",
                                       font=FONT_SMALL, text_color=PALETTE["warning"])
        self.status_dot.pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkFrame(sidebar, fg_color=PALETTE["border"], height=1).pack(fill="x", padx=12, pady=8)

        # Nav buttons
        self._nav_btns = {}
        nav_items = [
            ("dashboard",  "🏠  Dashboard"),
            ("students",   "👤  Étudiants"),
            ("subjects",   "📚  Matières"),
            ("stats",      "📊  Statistiques"),
        ]
        for key, label in nav_items:
            btn = ctk.CTkButton(
                sidebar, text=label, anchor="w",
                fg_color="transparent", hover_color=PALETTE["card"],
                text_color=PALETTE["text"], font=FONT_LABEL, height=40,
                command=lambda k=key: self._select(k)
            )
            btn.pack(fill="x", padx=8, pady=2)
            self._nav_btns[key] = btn

        # Bottom info
        ctk.CTkFrame(sidebar, fg_color=PALETTE["border"], height=1).pack(fill="x", padx=12, pady=8, side="bottom")
        ctk.CTkLabel(sidebar, text="Groupe 10  •  v2.0",
                     font=FONT_SMALL, text_color=PALETTE["muted"]).pack(side="bottom", pady=8)

        # Check server connection
        self.after(500, self._check_server)
        self.after(10000, self._poll_server)

    # ── Main content area ─────────────────────
    def _build_main(self):
        self.content = ctk.CTkFrame(self, fg_color=PALETTE["bg"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=0)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self._pages = {
            "dashboard": DashboardPage(self.content),
            "students":  StudentsPage(self.content),
            "subjects":  SubjectsPage(self.content),
            "stats":     StatsPage(self.content),
        }
        for page in self._pages.values():
            page.grid(row=0, column=0, sticky="nsew", padx=24, pady=20)
            page.grid_remove()

        self._current = None

    def _select(self, key):
        if self._current:
            self._pages[self._current].grid_remove()
            self._nav_btns[self._current].configure(fg_color="transparent",
                                                     text_color=PALETTE["text"])
        self._pages[key].grid()
        self._nav_btns[key].configure(fg_color=PALETTE["accent"],
                                       text_color="white")
        self._current = key
        # Refresh page data
        if hasattr(self._pages[key], "refresh"):
            self._pages[key].refresh()

    # ── Server status ─────────────────────────
    def _check_server(self):
        try:
            api_get("/students")
            self.status_dot.configure(text="●  Serveur OK", text_color=PALETTE["success"])
        except Exception:
            self.status_dot.configure(text="●  Hors ligne", text_color=PALETTE["danger"])

    def _poll_server(self):
        threading.Thread(target=self._check_server, daemon=True).start()
        self.after(10000, self._poll_server)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()