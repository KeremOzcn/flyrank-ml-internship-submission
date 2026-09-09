# Submission Checklist — FlyRank ML Internship

**Hazırlayan:** Kerem Özcan
**Tarih:** September 9, 2026
**Repo:** https://github.com/KeremOzcn/flyrank-ml-internship-submission
**Live site:** https://keremozcn.github.io/flyrank-ml-internship-submission/

---

## Tüm görevler ve linkleri

### Week 1 — Setup

| Kart | Görev | Dosya | GitHub Linki |
|---|---|---|---|
| FL-01 | Workflow Audit | `work/fl01_workflow_audit.md` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/fl01_workflow_audit.md |
| FL-02 | Portfolio Sitemap | `work/fl02_portfolio_sitemap.md` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/fl02_portfolio_sitemap.md |
| FL-03 | Proof Statement | `work/fl03_proof_statement.md` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/fl03_proof_statement.md |

### Week 2 — Framing

| Kart | Görev | Dosya | GitHub Linki |
|---|---|---|---|
| ML-02 | Research Question | `work/notebooks/w01_research_question.ipynb` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/notebooks/w01_research_question.ipynb |
| ML-03 | ML Task Framing | `work/notebooks/w02_ml_task_framing.ipynb` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/notebooks/w02_ml_task_framing.ipynb |

### Week 3 — Map & Face

| Kart | Görev | Dosya | GitHub Linki |
|---|---|---|---|
| CUSTOM-MQWZXUQU | Content Map & CTAs | `work/fl07_content_map.md` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/fl07_content_map.md |
| CUSTOM-MQX00WJN | Identity Kit | `work/fl05_identity_kit.md` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/fl05_identity_kit.md |
| CUSTOM-MQX033TI | Image Set & Rejection | `work/fl06_image_set.md` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/fl06_image_set.md |

### Week 4 — Pick the Stack

| Kart | Görev | Dosya/URL | Link |
|---|---|---|---|
| ML-07 | Stack Rationale + Empty but Live | `work/ml07_stack_rationale.md` + Live URL | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/ml07_stack_rationale.md |
| | Live URL | GitHub Pages | https://keremozcn.github.io/flyrank-ml-internship-submission/ |
| | Screenshot (home) | `work/capstone_home_screenshot.png` | Files alanına yüklenecek |

### Week 8 — Capstone

| Kart | Görev | Dosya/URL | Link |
|---|---|---|---|
| ML-CAP-01 | Capstone Report | `work/capstone_report.md` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/capstone_report.md |
| | Live Portfolio | GitHub Pages | https://keremozcn.github.io/flyrank-ml-internship-submission/ |
| | Contact form screenshot | `work/capstone_contact_form_screenshot.jpg` | Files alanına yüklenecek |
| | Home page screenshot | `work/capstone_home_screenshot.png` | Files alanına yüklenecek |

### FL-04 — Framed Cases (Week 2 ek)

| Kart | Görev | Dosya | GitHub Linki |
|---|---|---|---|
| FL-04 | Framed Cases | `work/fl04_framed_cases.md` | https://github.com/KeremOzcn/flyrank-ml-internship-submission/blob/main/work/fl04_framed_cases.md |

---

## Pipeline doğrulama

```bash
git clone https://github.com/KeremOzcn/flyrank-ml-internship-submission.git
cd flyrank-ml-internship-submission
pip install -r requirements.txt
python scripts/run_all.py
```

Çıktılar:
- `outputs/model_results.json` — tüm metrikler
- `outputs/refresh_queue.csv` — ranked review queue
- `outputs/model_report.md` — Markdown report
- `outputs/charts/*.svg` — 5 chart
- `outputs/flyrank_refresh_model_results.pdf` — PDF

---

## Formspree test

- Endpoint: `xbgjqdrw` (Kerem'in hesabı)
- Test gönderildi: ✅ "Thanks — your message reached me" mesajı alındı
- Formspree inbox: https://formspree.io/forms/xbgjqdrw/submissions

---

## Notlar

- Tüm metrikler September 9, 2026 tarihinde `python scripts/run_all.py` ile üretilmiştir
- FL-02 ve FL-03'ün orijinal "~3x" claim'leri düzeltilmiş, measured baseline failure + verified model result ile değiştirilmiştir
- Capstone report 9 bölümü tam doldurulmuş, tüm sayılar `outputs/model_results.json`'dan gelmektedir
- Portfolio sitesi 4 sayfadan oluşur: Home, Work, How I Work, Contact
- Contact form Formspree free tier ile çalışmaktadır, server gerektirmez