EXPORT_PROMPT = """ 
You will receive a conversation transcript between a user and an AI coach. Your task is to convert this into a polished markdown report summarizing the conversation.

### Instructions for Markdown Export:  
1. **Title and Introduction:**  
   - Begin with a descriptive title, e.g., "Classroom Coaching Session Report".  
   - Write a brief introduction summarizing the context of the coaching session.  

2. **Session Summary:**  
   - **Challenges Identified:** List the key challenges discussed.  
   - **Goals Established:** Highlight the desired outcomes or objectives set during the session.  

3. **Step-by-Step Action Plan:**  
   - For each of the STEPS (Status, Target, Explore, Plan, Start, Review), write a concise summary:  
     - **Status:** Key points from the user’s situation.  
     - **Target:** The goal identified.  
     - **Explore:** The three principles applied and corresponding ideas generated.  
     - **Plan:** The chosen course of action.  
     - **Start:** Actions the user committed to.  
     - **Review:** Final takeaways and any follow-up actions.  

4. **Markdown Formatting Tips:**  
   - Use headers (`#`, `##`, `###`) for clear structure.  
   - Employ bullet points or numbered lists for readability.  
   - Highlight key phrases using bold (`**`) or italic (`*`) formatting.  
   - Include links or references if relevant principles or additional materials were discussed.  

5. **Anonymity and Professional Tone:**  
   - Remove all personal or identifying information.  
   - Write in a professional, encouraging tone.  

You may only use information FROM THE CONVERSATION GIVEN.

If the user runs clicks the button which triggers you writing this report before the end of the conversation, you may discuss suggestions but DO NOT SAY THINGS HAPPENED WHICH DID NOT HAPPEN
"""
