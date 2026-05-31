import express from "express";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static("public"));

app.post("/translate", async (req, res) => {
  try {
    const { text, targetLanguage } = req.body;

    const response = await fetch(
      "https://openrouter.ai/api/v1/chat/completions",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "openai/gpt-4o-mini",
          messages: [
            {
              role: "user",
              content: `Translate the following text into ${targetLanguage}. Return only the translation:\n\n${text}`
            }
          ]
        })
      }
    );

    const data = await response.json();

    const translatedText =
      data.choices?.[0]?.message?.content || "Translation failed";

    res.json({ translatedText });

  } catch (error) {
    console.error(error);
    res.status(500).json({
      translatedText: "Error translating text"
    });
  }
});

app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});