# 🎬 Dr. Document Demo & Examples

This document provides examples and demonstrations of Dr. Document's capabilities.

## 🚀 Quick Demo

### Step 1: Start the Application

**Terminal 1 - Backend:**
```bash
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

### Step 2: Process a Repository

1. Open your browser to `http://localhost:5173`
2. Enter a GitHub repository URL:
   - Example: `https://github.com/username/small-project`
   - Try with a repository that has 5-20 files for best demo experience

3. Click "🚀 Generate Documentation"

4. Watch the agents work in real-time:
   - **Code Reader** 👀 - Analyzes each file
   - **Requirements Extractor** 📋 - Extracts requirements
   - **Manager** 👔 - Reviews quality
   - **README Writer** ✍️ - Generates documentation
   - **Final Reviewer** 🔍 - Validates completeness

5. View the generated README with quality scores

## 📊 Example Output

### Agent Workspace View

```
🏢 Agent Office
Multi-Agent AI System at Work

Overall Progress: 75%
Status: Writing README...

[Agent Cards showing real-time status]
👀 Code Reader - ✅ Completed
📋 Requirements Extractor - ✅ Completed
👔 Manager - ✅ Completed
✍️ README Writer - ⚙️ Working...
🔍 Final Reviewer - ⏸️ Idle
```

### Sample Generated README Structure

```markdown
# 🚀 Project Name

AI-generated comprehensive documentation

## 📝 Description
[Clear overview of the project]

## ✨ Features
- Feature 1
- Feature 2
- Feature 3

## 🛠️ Technical Stack
- Technology 1
- Technology 2
- Technology 3

## 🏗️ Architecture
[Description of architecture patterns]

## 📦 Installation
[Setup instructions]

## 💡 Usage
[Usage examples]

## 🤝 Contributing
[Contribution guidelines]
```

## 📋 Logging Output Examples

### Console Output with Colors

```
[2026-02-19 11:00:00.000] [INFO] 🎯 Starting workflow for https://github.com/user/repo
[2026-02-19 11:00:01.000] [INFO] 🔵 Cloning repository...
[2026-02-19 11:00:05.000] [SUCCESS] 🟢 Successfully cloned repository
[2026-02-19 11:00:06.000] [INFO] 📁 Found 15 files to process
[2026-02-19 11:00:07.000] [INFO] 🤖 [AGENT START] Code Reader: Processing input
[2026-02-19 11:00:08.000] [INFO] 📥 [LLM INPUT] Model: LongCat-Flash-Lite
[2026-02-19 11:00:09.000] [INFO] 🤖 [LLM CALL] Model: LongCat-Flash-Lite, Details: {...}
[2026-02-19 11:00:12.000] [INFO] 📤 [LLM OUTPUT] Model: LongCat-Flash-Lite
[2026-02-19 11:00:13.000] [SUCCESS] ✅ [AGENT COMPLETE] Code Reader: Successfully processed
```

### Log File (`backend/dr_document.log`)

All operations are logged with timestamps for audit trail:

```
[2026-02-19 11:00:00.123] [INFO] 🎯 Starting workflow for https://github.com/user/repo
[2026-02-19 11:00:01.456] [INFO] 📁 [FILE] Discovered: src/main.py
[2026-02-19 11:00:02.789] [INFO] 📥 [LLM INPUT] Model: LongCat-Flash-Lite
[2026-02-19 11:00:03.012] [INFO] 🤖 [LLM CALL] Model: LongCat-Flash-Lite
[2026-02-19 11:00:05.345] [INFO] 📤 [LLM OUTPUT] Model: LongCat-Flash-Lite
```

## 🎯 Testing Different Repository Types

### Small Python Project (5-10 files)
- Best for quick demos
- Processes in 1-2 minutes
- Good for testing basic functionality

### Medium Project (10-20 files)
- Standard use case
- Processes in 2-4 minutes
- Shows full workflow capabilities

### Large Project (20-30 files)
- Comprehensive analysis
- Processes in 4-6 minutes
- Demonstrates scalability (limited to 30 files by default)

## 🔧 API Testing with curl

### Start Processing
```bash
curl -X POST http://localhost:8000/api/process-repo \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/user/repo"}'
```

Response:
```json
{
  "job_id": "abc123...",
  "status": "pending",
  "message": "Repository processing started"
}
```

### Check Status
```bash
curl http://localhost:8000/api/status/abc123...
```

Response:
```json
{
  "job_id": "abc123...",
  "status": "analyzing",
  "progress": 45,
  "message": "Analyzing code files..."
}
```

### Get Result
```bash
curl http://localhost:8000/api/result/abc123...
```

Response:
```json
{
  "job_id": "abc123...",
  "repo_name": "user/repo",
  "readme": "# Project Documentation\n...",
  "files_analyzed": 15,
  "manager_review": {
    "approved": true,
    "quality_score": 85
  },
  "final_review": {
    "approved": true,
    "completeness_score": 90,
    "accuracy_score": 88
  }
}
```

## 🐛 Troubleshooting Demo Issues

### Backend Won't Start
- Check if `.env` file exists with LONGCAT_API_KEY
- Verify Python version (3.9+)
- Check if port 8000 is available

### Frontend Won't Connect
- Ensure backend is running first
- Check CORS settings
- Verify API URL in `.env` (VITE_API_URL)

### LLM Errors
- Verify LONGCAT_API_KEY is valid
- Check API key has sufficient token quota
- Review backend logs for detailed error messages

### WebSocket Connection Issues
- Check browser console for connection errors
- Ensure backend WebSocket endpoint is accessible
- Verify firewall/proxy settings

## 💡 Tips for Best Results

1. **Choose Appropriate Repositories**:
   - Start with small, well-documented repos
   - Avoid repos with only configuration files
   - Prefer repos with clear structure

2. **Monitor the Logs**:
   - Check `backend/dr_document.log` for detailed info
   - Watch console output for real-time updates
   - Look for LLM interaction logs

3. **Quality Scores**:
   - Scores above 80 indicate high-quality analysis
   - Scores between 60-80 are acceptable
   - Scores below 60 may need manual review

4. **Token Usage**:
   - Flash-Lite is used for most operations (efficient)
   - Flash-Thinking is used for complex reviews
   - Flash-Chat is used for content generation

## 🎓 Learning Examples

### Example 1: Simple Python Script Repository
- URL: Small Python project with 3-5 `.py` files
- Expected time: 1-2 minutes
- Focus: Code structure analysis

### Example 2: React Component Library
- URL: React project with `.tsx` and `.jsx` files
- Expected time: 2-3 minutes
- Focus: Component documentation

### Example 3: Full-Stack Application
- URL: Project with frontend and backend
- Expected time: 3-5 minutes
- Focus: Architecture and tech stack

## 🔍 What to Look For

1. **Real-time Updates**: Agent cards should update in real-time
2. **Progress Bar**: Should smoothly increase from 0-100%
3. **Color-coded Logs**: Console should show colored, emoji-rich logs
4. **Generated README**: Should be well-formatted Markdown
5. **Quality Scores**: All scores should be displayed with metrics

## 📸 Screenshots to Capture

- Initial repo input screen
- Agent workspace with agents working
- Progress bar at various stages
- Generated README preview
- Quality score display

## 🎉 Success Indicators

✅ All agents complete successfully
✅ README is generated and displayed
✅ Quality scores are reasonable (>60)
✅ WebSocket updates work smoothly
✅ Logs show comprehensive information
✅ Export/download functions work

Happy documenting! 🏥📝
