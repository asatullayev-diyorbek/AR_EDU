"""Gemini AI chat endpoint."""
import logging

from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.utils.response import error_response, success_response

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Siz Diyora AR Edu ta'lim platformasining AI yordamchisisiz. "
    "Foydalanuvchilarga o'quv materiallari, AR texnologiyasi, dasturlash va fan bo'yicha "
    "yordam bering. Javoblaringiz qisqa, aniq va o'zbek tilida bo'lsin. "
    "Agar savol ta'lim bilan bog'liq bo'lmasa, muloyimlik bilan yordamchi bo'lishga harakat qiling."
)


class AIChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = (request.data.get("message") or "").strip()
        if not message:
            return error_response(message="Message is required.", code=400)

        api_key = getattr(settings, "GEMINI_API_KEY", "")
        if not api_key:
            return error_response(
                message="Gemini API key sozlanmagan. .env faylida GEMINI_API_KEY ni qo'shing.",
                code=503,
            )

        model = getattr(settings, "GEMINI_MODEL", "gemini-2.0-flash")

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model,
                contents=message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                ),
            )
            return success_response(data={"reply": response.text}, message="OK")

        except Exception as exc:
            status = getattr(exc, "status_code", None)
            if status == 429:
                return error_response(
                    message="So'rov limiti oshdi. Bir oz kutib qayta urinib ko'ring.",
                    code=429,
                )
            logger.exception("Gemini API error: %s", exc)
            return error_response(message="AI javob berishda xato yuz berdi.", code=500)
