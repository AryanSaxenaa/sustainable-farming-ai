export async function fetchAdvice(userInput) {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/advice', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: userInput })
      });
      return await response.json();
    } catch (error) {
      console.error("Error fetching advice:", error);
      return { advice: "Error contacting backend." };
    }
  }
  