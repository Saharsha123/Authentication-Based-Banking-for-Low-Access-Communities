# Authentication-Based-Banking-for-Low-Access-Communities
## 📌 Overview
Authentication-Based Banking for Low-Access Communities is a secure, inclusive banking system that simplifies low-value transactions for users facing barriers to traditional banking.
It reduces reliance on literacy-intensive processes through OTP and biometric authentication, delivering fast, safe access—especially in rural and semi-urban areas.
Built via a Design Thinking approach, this project boosts financial independence for those with limited digital or reading skills.

## 🎯 Problem Statement
Traditional banking excludes low-access communities due to:
* Illiteracy or limited reading skills
* Complex, paper-heavy processes
* Reliance on intermediaries for transactions
* Long waits and error-prone handling
These barriers widen the gap between financial services and underserved users.

## 🚀 Objectives
* Deliver intuitive interfaces to simplify banking
* Enable secure, authentication-based transactions (OTP + biometrics)
* Eliminate paperwork and intermediary dependence
* Boost accessibility in rural and semi-urban areas
* Ensure fast, safe low-value payments

## 💡 Proposed Solution
Users perform low-value banking transactions via secure authentication—no complex forms required.
Key Features:
- 🔐 Biometric authentication (fingerprint or face ID)
- 📱 OTP-based verification
- 🖥️ Minimal-text, intuitive interface
- ✅ Automated account validation
- ⚡ Real-time transaction confirmations
- 📄 Instant bill and receipt generation

## 🧠 System Workflow
```
LOGIN (Biometrics/OTP)
    ↓
VALID? ── NO ──> [Error: Invalid Credentials]
    ↓ YES
DASHBOARD + FORM
    ↓
ENTER ACCOUNT/AMOUNT
    ↓
VALIDATE BALANCE/LIMITS? ── NO ──> [Error: Insufficient Funds/Limit Exceeded]
    ↓ YES
GENERATE OTP ──> USER INPUT
    ↓
OTP VALID? ── NO ──> [Error: Invalid OTP] ──┐
    ↓ YES                                   │ 
TRANSACTION EXECUTED                        │ (Retry up to 3x)
    ↓                                       │
RECEIPT GENERATED <─────────────────────────┘
    ↓
[Transaction Complete]

```

## 🏗️ Tech Stack
| Category                  | Technologies                                             |
| ------------------------- | -------------------------------------------------------- |
| Frontend                  | HTML, CSS, JavaScript, React.js / Vue.js                 |
| Backend                   | Node.js, Python (Flask/Django)                           |
| Database                  | MySQL, PostgreSQL                                        |
| Security & Authentication | OTP verification, Biometric integration, Data encryption |

## 👨‍💻 Contributors
- Saharsha | Koushik Nayaka | Mayur Kiran Kumar
- R. V. College of Engineering
- Department of Computer Science Engineering
