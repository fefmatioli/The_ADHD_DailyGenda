# README.md — DailyGenda

## 📌 Descrição do Projeto

O **DailyGenda** é um sistema web desenvolvido em **Django**, utilizando **PostgreSQL** como banco de dados e oferecendo interface via **templates HTML**. O sistema permite que cada usuário gerencie:

- Notas  
- Eventos  
- Tarefas  

Além disso, o projeto possui uma **API REST completa**, construída com Django REST Framework, com autenticação obrigatória e suporte a **JWT**.

O objetivo é oferecer tanto uma aplicação web funcional quanto uma API estruturada para integrações futuras.

---

## 🧱 Arquitetura do Projeto

### **1. Frontend (Django Templates)**

Localização: `core/templates/`

Contém:

- `login.html`
- `signup.html`
- `dashboard.html`
- `event_detail.html` / `event_edit.html`
- `note_detail.html` / `note_edit.html`

Essas páginas são renderizadas pelas views em:

```
core/views_site.py
```

### **2. Backend (API REST)**

Localização:

```
core/views.py
core/serializers.py
```

Endpoints expostos:

| Recurso | Endpoint | Método | Descrição |
|--------|----------|--------|-----------|
| Notes  | `/api/notes/` | GET/POST/PUT/PATCH/DELETE | Gestão de notas |
| Events | `/api/events/` | GET/POST/PUT/PATCH/DELETE | Gestão de eventos |
| Tasks  | `/api/tasks/` | GET/POST/PUT/PATCH/DELETE | Gestão de tarefas |

A API usa:

- `ModelViewSet`
- `IsAuthenticated`
- `OwnerQuerysetMixin`, garantindo que cada usuário só acessa seus próprios dados
- Filtros de data, categoria e status

JWT é suportado pelos endpoints:

```
/api/token/
/api/token/refresh/
```

---

## 🗄️ Banco de Dados (PostgreSQL)

### 📌 Criando o banco e o usuário

Execute no pgAdmin ou psql:

```sql
CREATE DATABASE dailygenda;
CREATE USER dailygenda_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE dailygenda TO dailygenda_user;
GRANT USAGE, CREATE ON SCHEMA public TO dailygenda_user;
```

---

## 🔐 Arquivo `.env`

Crie um arquivo `.env` na pasta principal do projeto (mesmo nível do `manage.py`):

```
DB_NAME=dailygenda
DB_USER=dailygenda_user
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

Esse arquivo **não deve ser enviado ao GitHub**.

---

## ⚙️ Como rodar o projeto

### **1. Criar ambiente virtual**

```bash
python -m venv venv
```

### **2. Ativar**

Windows:

```bash
.venv\Scripts\activate
```

### **3. Instalar dependências**

```bash
pip install -r requirements.txt
```

### **4. Aplicar migrações**

```bash
python manage.py migrate
```

### **5. Criar superusuário**

```bash
python manage.py createsuperuser
```

### **6. Rodar o servidor**

```bash
python manage.py runserver
```

Acesso:

- Site: http://localhost:8000/dashboard/  
- Login: http://localhost:8000/login/  
- API: http://localhost:8000/api/notes/  

---

## 🔑 Autenticação

### Sessão (Site)

O site usa autenticação padrão do Django (`LoginView` + cookies de sessão).

### JWT (API)

Obter token:

```
POST /api/token/
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

Usar token:

```
Authorization: Bearer <token>
```

---

## 🧪 Funcionalidades

### Dashboard

- Lista notas, tarefas e eventos do usuário atual  
- Botões para criar, editar e excluir  

### API

- CRUD completo para Notes, Events e Tasks  
- Filtragem por data, categoria e status  
- Segurança via JWT  
- Isolamento por usuário  

---

## 📂 Estrutura do Projeto

```
Project_Django_TDS/
│
├── api_project/
│   ├── core/
│   │   ├── models.py
│   │   ├── views.py            # API REST
│   │   ├── views_site.py       # Páginas HTML
│   │   ├── serializers.py
│   │   ├── forms.py
│   │   ├── templates/
│   │   └── static/
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   └── manage.py
│
├── requirements.txt
```

---