from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from .vector_helper import semantic_search
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, \
    ChatCompletionUserMessageParam

import os

open_ai_client = OpenAI(api_key=os.environ.get("OPENAI_SECRET_KEY"))

class AssistantQAView(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):

        question = request.data.get("question")
        if not question:
            return Response({"error": "Missing 'question' field."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Step 1: Search relevant provider data from vector DB
            search_results = semantic_search("providers", question, top_k=5)
            context_chunks = search_results.get("documents", [[]])[0]
            context = "\n\n".join(context_chunks)

            # Step 2: Construct system + user messages
            messages: list[ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam] = [
                ChatCompletionSystemMessageParam(role="system", content="You are a helpful assistant that can help users get info about car service centers."
                                                                        "You can answer only the questions regarding the can service centers, working hours, services provided by the center etc."
                                                                        "If you don't have data then you should be polite and tell the user that you don't have that information."
                                                                        "If the user is asking about services provided by the provider you can only answer the services provided by the provider."
                                                                        "And if you don't know what is included in the service, you can only answer the Service name."
                                                                        "The included features can be included or not, you need to answer only included features"),
                ChatCompletionUserMessageParam(role="user", content=f"Context:\n{context}\n\nQuestion:\n{question}",)
            ]

            # Step 3: Call OpenAI chat completion
            chat_response = open_ai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.2,
            )

            answer = chat_response.choices[0].message.content.strip()

            return Response({"answer": answer})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
