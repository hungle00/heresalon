import React, { useState, useRef, useEffect } from 'react';

/**
 * ChatWidget
 * Props (optional):
 * - onDispatch(message): called immediately when user sends a message (message object)
 * - sendMessageToApi(message): async function to call API; should return bot response
 * - onResponse(botMessage): called when bot response is available
 */
const ChatWidget = ({ onDispatch, sendMessageToApi, onResponse }) => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { id: 1, from: 'bot', text: 'Hi! How can we help you today?' },
  ]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [awaitingResponse, setAwaitingResponse] = useState(false);
  const idRef = useRef(2);
  const timeoutRef = useRef(null);

  const addMessage = (msg) => {
    setMessages((m) => {
      const next = [...m, msg];
      // Keep only the last 30 messages
      if (next.length > 30) return next.slice(next.length - 30);
      return next;
    });
  };

  const messagesRef = useRef(null);

  // Auto-scroll to bottom whenever messages or typing indicator changes
  useEffect(() => {
    const el = messagesRef.current;
    if (!el) return;
    // scroll to bottom
    el.scrollTop = el.scrollHeight;
  }, [messages, isBotTyping]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text) return;
    // Don't allow sending if we're waiting for bot response (turn-taking)
    if (awaitingResponse) return;

    const userMsg = { id: idRef.current++, from: 'user', text };
    // Dispatch immediately (e.g., to show pending state or store)
    addMessage(userMsg);
    setInput('');
    if (onDispatch) {
      try { onDispatch(userMsg); } catch (e) { /* caller can handle */ }
    }

    // Show bot typing animation and mark awaiting
    setIsBotTyping(true);
    setAwaitingResponse(true);

    // Setup timeout fallback: if no response in 5s, add auto-reply
    let timedOut = false;
    timeoutRef.current = setTimeout(() => {
      timedOut = true;
      const fallback = { id: idRef.current++, from: 'bot', text: 'The connection is low' };
      addMessage(fallback);
      setIsBotTyping(false);
      setAwaitingResponse(false);
    }, 5000);

    // If provided, call sendMessageToApi and await response; otherwise simulate
    try {
      let botResp = null;
      if (sendMessageToApi) {
        // sendMessageToApi should be an async function returning bot message object or text
        botResp = await sendMessageToApi(userMsg);
      } else {
        // Simulate delay and response
        await new Promise((r) => setTimeout(r, 1400));
        botResp = { id: idRef.current++, from: 'bot', text: "Thanks — we'll get back to you shortly." };
      }
      // If timed out already (fallback ran), don't append duplicate
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }

      if (!timedOut) {
        // Call onResponse callback
        if (onResponse) {
          try { onResponse(botResp); } catch (e) { /* caller */ }
        }

        // Append bot response
        if (botResp) addMessage(typeof botResp === 'string' ? { id: idRef.current++, from: 'bot', text: botResp } : botResp);
      }
    } catch (err) {
      // Optionally append an error message
      if (timeoutRef.current) { clearTimeout(timeoutRef.current); timeoutRef.current = null; }
      addMessage({ id: idRef.current++, from: 'bot', text: 'Sorry, something went wrong.' });
    } finally {
      setIsBotTyping(false);
      setAwaitingResponse(false);
    }
  };

  // cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  return (
    <>
      <div className="fixed right-6 bottom-6 z-50">
        {!open && (
          <button
            onClick={() => setOpen(true)}
            aria-label="Open chat"
            className="w-14 h-14 rounded-full bg-pink-600 text-white shadow-lg flex items-center justify-center hover:bg-pink-700 transition-colors"
          >
            <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M21 12c0 4.418-4.03 8-9 8a9.77 9.77 0 01-4-.85L3 21l1.15-4.15A7.72 7.72 0 013 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </button>
        )}

        {open && (
          <div className="w-80 max-w-xs bg-white rounded-lg shadow-xl overflow-hidden flex flex-col">
            <div className="flex items-center justify-between px-4 py-2 bg-pink-600 text-white">
              <div className="font-medium">Chat with us</div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setOpen(false)}
                  aria-label="Back"
                  className="p-1 rounded hover:bg-pink-500/20"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <button
                  onClick={() => setOpen(false)}
                  aria-label="Close"
                  className="p-1 rounded hover:bg-pink-500/20"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Increased height: doubled from 48 to 96 (h-96). Use max-h to cap and allow scrolling */}
            <div ref={messagesRef} className="p-3 flex-1 max-h-96 overflow-auto text-sm text-gray-700 flex flex-col">
              <div className="text-gray-500 text-xs mb-2">This is a demo chat. Replace with your chat provider or websocket logic.</div>

              <div className="flex-1 space-y-3">
                {messages.map((m) => (
                  <div key={m.id} className={`flex ${m.from === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`${m.from === 'user' ? 'bg-pink-600 text-white' : 'bg-gray-100 text-gray-800'} px-3 py-2 rounded-lg max-w-[80%]`}>{m.text}</div>
                  </div>
                ))}

                {/* Typing animation for bot (three dots) */}
                {isBotTyping && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 px-3 py-2 rounded-lg inline-flex items-center">
                      <span className="dot bounce bg-gray-500 w-2 h-2 rounded-full mr-1 inline-block"></span>
                      <span className="dot bounce bg-gray-500 w-2 h-2 rounded-full mr-1 inline-block" style={{ animationDelay: '0.12s' }}></span>
                      <span className="dot bounce bg-gray-500 w-2 h-2 rounded-full inline-block" style={{ animationDelay: '0.24s' }}></span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="p-2 border-t border-gray-100">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type a message..."
                  onKeyDown={(e) => { if (e.key === 'Enter') handleSend(); }}
                  className="flex-1 px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-pink-500"
                />
                <button onClick={handleSend} className="bg-pink-600 text-white px-3 py-2 rounded-md text-sm">Send</button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Inline styles for typing animation (kept here to avoid touching global CSS) */}
      <style>{`
        .dot { display:inline-block }
        .bounce { animation: chat-bounce 1s infinite; }
        @keyframes chat-bounce {
          0% { transform: translateY(0); opacity: 0.6 }
          50% { transform: translateY(-4px); opacity: 1 }
          100% { transform: translateY(0); opacity: 0.6 }
        }
      `}</style>
    </>
  );
};

export default ChatWidget;
