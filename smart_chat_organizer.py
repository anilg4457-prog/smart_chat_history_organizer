import argparse
import os
import json
from datetime import datetime

def parse_whatsapp_chat(file_path):
    chats = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                date_part, msg_part = line.strip().split(" - ", 1)
                timestamp = datetime.strptime(date_part, "%d/%m/%Y, %H:%M")
                sender, message = msg_part.split(": ", 1)
                chats.append({
                    "time": timestamp,
                    "sender": sender.strip(),
                    "message": message.strip()
                })
            except ValueError:
                continue
    return chats


def generate_summary(chats):
    summary = {}
    for chat in chats:
        sender = chat["sender"]
        if sender not in summary:
            summary[sender] = {
                "total_messages": 0,
                "first_message_time": chat["time"],
                "last_message_time": chat["time"],
                "sample_messages": []
            }
        summary[sender]["total_messages"] += 1
        summary[sender]["last_message_time"] = chat["time"]
        if len(summary[sender]["sample_messages"]) < 2:
            summary[sender]["sample_messages"].append(chat["message"])
    return summary


def print_ascii_chart(summary):
    print("\nSmart Chat History Organizer — Summary")
    total_msgs = sum(v["total_messages"] for v in summary.values())
    print(f"Total messages: {total_msgs}")
    print(f"Total unique senders: {len(summary)}")

    most_active = max(summary.items(), key=lambda x: x[1]["total_messages"])
    print(f"Most active sender: {most_active[0]} ({most_active[1]['total_messages']})\n")

    print("Top 5 Senders:")
    for sender, data in summary.items():
        bars = "#" * (data["total_messages"] * 10)
        print(f"{sender:<10} | {bars} ({data['total_messages']})")


def save_outputs(summary, outdir):
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "user_summary.json"), "w", encoding='utf-8') as jf:
        json.dump(summary, jf, indent=2, default=str)

    with open(os.path.join(outdir, "summary.txt"), "w", encoding='utf-8') as tf:
        tf.write("Smart Chat History Organizer — Summary\n")
        total_msgs = sum(v["total_messages"] for v in summary.values())
        tf.write(f"Total messages: {total_msgs}\n")
        tf.write(f"Total unique senders: {len(summary)}\n\n")
        most_active = max(summary.items(), key=lambda x: x[1]["total_messages"])
        tf.write(f"Most active sender: {most_active[0]} ({most_active[1]['total_messages']})\n\n")
        tf.write("Top 5 Senders:\n")
        for sender, data in summary.items():
            bars = "#" * (data["total_messages"] * 10)
            tf.write(f"{sender:<10} | {bars} ({data['total_messages']})\n")


def main():
    parser = argparse.ArgumentParser(description="Smart Chat History Organizer")
    parser.add_argument("--input", required=True, help="Chat log file path")
    parser.add_argument("--format", default="whatsapp", choices=["auto", "whatsapp", "pipe", "bracket"])
    parser.add_argument("--outdir", default="output", help="Output directory")
    parser.add_argument("--filter-keyword", help="Filter messages containing keyword")
    parser.add_argument("--from-date", help="Filter messages after this date (YYYY-MM-DD)")
    parser.add_argument("--to-date", help="Filter messages before this date (YYYY-MM-DD)")
    args = parser.parse_args()

    chats = parse_whatsapp_chat(args.input)

    # Apply date filters
    if args.from_date:
        start = datetime.strptime(args.from_date, "%Y-%m-%d")
        chats = [c for c in chats if c["time"] >= start]

    if args.to_date:
        end = datetime.strptime(args.to_date, "%Y-%m-%d")
        chats = [c for c in chats if c["time"] <= end]

    # Apply keyword filter
    if args.filter_keyword:
        keyword = args.filter_keyword.lower()
        chats = [
            c for c in chats
            if keyword in c["message"].lower() or keyword in c["sender"].lower()
        ]

    # ✅ Optional feature: Save filtered messages to a text file
    if (args.filter_keyword or args.from_date or args.to_date) and chats:
        filtered_path = os.path.join(args.outdir, "filtered_messages.txt")
        os.makedirs(args.outdir, exist_ok=True)
        with open(filtered_path, "w", encoding="utf-8") as f:
            f.write("Filtered Messages:\n\n")
            for chat in chats:
                time_str = chat["time"].strftime("%Y-%m-%d %H:%M")
                f.write(f"[{time_str}] {chat['sender']}: {chat['message']}\n")

    summary = generate_summary(chats)

    if not summary:
        print("⚠️ No valid messages found in input file. Check format!")
        return

    save_outputs(summary, args.outdir)
    print_ascii_chart(summary)


if __name__ == "__main__":
    main()
