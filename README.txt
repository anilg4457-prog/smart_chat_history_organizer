SMART CHAT HISTORY ORGANIZER



Usage:
------
python smart_chat_organizer.py --input sample_chats/whatsapp_chat.txt --format whatsapp --outdir results

Options:
--------
--input <file>         Chat log file path
--outdir <dir>         Output directory (default: output)
--format <auto|whatsapp|pipe|bracket>
--filter-keyword <word>   Filter messages containing keyword
--from-date YYYY-MM-DD    Filter messages after this date
--to-date YYYY-MM-DD      Filter messages before this date

Outputs:
--------
- user_summary.json — JSON per-user stats
- summary.txt       — Human readable summary with ASCII chart
- filtered_messages.txt (optional)



summary.txt (Human-readable report)

Smart Chat History Organizer — Summary
Total messages: 4
Total unique senders: 3
Most active sender: Anu (2)

Top 5 Senders:
Anu     | #################### (2)
Babu        | ########## (1)
Chitra      | ########## (1)




user_summary.json (Detailed structured data)

Output Example:

{
  "Anu": {
    "total_messages": 2,
    "first_message_time": "2025-10-12T09:15:00",
    "last_message_time": "2025-10-12T09:17:00",
    "sample_messages": [
      "Hi! Are you coming today?",
      "Great!"
    ]
  },
  "Babu": {
    "total_messages": 1,
    "first_message_time": "2025-10-12T09:16:00",
    "last_message_time": "2025-10-12T09:16:00",
    "sample_messages": [
      "Yes, I'll be there."
    ]
  },
  "Chitra": {
    "total_messages": 1,
    "first_message_time": "2025-10-12T09:20:00",
    "last_message_time": "2025-10-12T09:20:00",
    "sample_messages": [
      "See you both there!"
    ]
  }
}
