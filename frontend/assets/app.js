// 프론트 ↔ 백엔드 연동 헬퍼 (소유자: 박태준)
// 백엔드 계약: POST /api/chat  (schemas.py 의 ChatRequest/ChatResponse)

async function sendChat(message, { lat = null, lng = null, history = [] } = {}) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, lat, lng, history }),
  });
  if (!res.ok) throw new Error("서버 오류: " + res.status);
  return res.json(); // { reply, emergency, need_more_info, departments[], hospitals[] }
}

// 사용 예시 (chat.html 에서 연결):
// const out = await sendChat("오른쪽 아랫배가 아프고 열이 나요");
// if (out.emergency) { /* 119 안내 표시 */ }
// else { renderDepartments(out.departments); }

window.DrRouter = { sendChat };
