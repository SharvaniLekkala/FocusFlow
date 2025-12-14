import { useEffect, useState } from "react";
import { getToken, logout } from "../utils/auth";
import {
  createSession,
  getSessions,
  getInsights,
  clearTodaySessions,
  getSummary,
} from "../api";

function Dashboard() {
  const token = getToken();

  const [task, setTask] = useState("");
  const [duration, setDuration] = useState("");
  const [sessions, setSessions] = useState([]);
  const [insights, setInsights] = useState(null);
  const [weekly, setWeekly] = useState(null);
  const [monthly, setMonthly] = useState(null);

  useEffect(() => {
    if (token) {
      fetchData();
    }
  }, [token]);

  const fetchData = async () => {
    const sessionsRes = await getSessions(token);
    setSessions(sessionsRes.data);

    const insightsRes = await getInsights(token);
    setInsights(insightsRes.data);

    const weekRes = await getSummary("week", token);
    setWeekly(weekRes.data);

    const monthRes = await getSummary("month", token);
    setMonthly(monthRes.data);
  };

  const addSession = async () => {
    if (!task || !duration) return;

    await createSession(
      { task_name: task, duration: Number(duration) },
      token
    );

    setTask("");
    setDuration("");
    fetchData();
  };

  const clearToday = async () => {
    await clearTodaySessions(token);
    fetchData();
  };

  if (!token) return <h3>Please login to view dashboard</h3>;

  return (
    <div>
      <h2>Dashboard</h2>

      {/* Add Session */}
      <h3>Add Focus Session</h3>
      <input
        placeholder="Task name"
        value={task}
        onChange={(e) => setTask(e.target.value)}
      />
      <input
        type="number"
        placeholder="Minutes"
        value={duration}
        onChange={(e) => setDuration(e.target.value)}
      />
      <button onClick={addSession}>Add</button>

      {/* Clear Today */}
      <div style={{ marginTop: "10px" }}>
        <button onClick={clearToday}>Clear Today's Sessions</button>
      </div>

      {/* Insights */}
      {insights && (
        <div>
          <h3>Productivity Insights</h3>
          <p>{insights.summary}</p>
          <p>
            <b>Total Focus:</b> {insights.total_minutes} minutes
          </p>
          <p>
            <b>Average Session:</b> {insights.average_session} minutes
          </p>
        </div>
      )}

      {/* Weekly Summary */}
      {weekly && (
        <div>
          <h3>Weekly Summary</h3>
          <p>Total Focus: {weekly.total_minutes} minutes</p>
          <p>Average Daily Focus: {weekly.average_daily_minutes} minutes</p>
          <p>Days Tracked: {weekly.days_tracked}</p>
        </div>
      )}

      {/* Monthly Summary */}
      {monthly && (
        <div>
          <h3>Monthly Summary</h3>
          <p>Total Focus: {monthly.total_minutes} minutes</p>
          <p>Average Daily Focus: {monthly.average_daily_minutes} minutes</p>
          <p>Days Tracked: {monthly.days_tracked}</p>
        </div>
      )}

      {/* Sessions List */}
      <h3>Your Focus Sessions</h3>
      <ul>
        {sessions.map((s) => (
          <li key={s.id}>
            {s.task_name} — {s.duration} mins
          </li>
        ))}
      </ul>

      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default Dashboard;
