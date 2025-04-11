// import React from 'react';

// const VoiceQuery = ({ setQuery }) => {
//   const handleVoice = () => {
//     const recognition = new window.webkitSpeechRecognition();
//     recognition.lang = 'en-US';
//     recognition.onresult = (event) => {
//       const transcript = event.results[0][0].transcript;
//       setQuery(transcript);
//     };
//     recognition.start();
//   };

//   return (
//     <button onClick={handleVoice} className="mt-2 bg-blue-500 text-white px-4 py-2 rounded">
//       Speak Query 🎤
//     </button>
//   );
// };

// export default VoiceQuery;