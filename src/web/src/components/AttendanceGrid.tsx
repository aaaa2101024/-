import { useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

interface Attendance {
    id: number;
    name: string;
    status: string;
    updated_at: string;
}

const WEBSOCKET_URL = "ws://localhost:8000/ws/attendance";

const STATUS_LIST: string[] = ["在室", "休憩中", "退室"];

const AttendanceGrid = () => {
    const [attendances, setAttendances] = useState<Attendance[]>([]);
    const { lastMessage, readyState } = useWebSocket(WEBSOCKET_URL);

    // FastAPIからメッセージが送信されるたびに在室状況を更新
    useEffect(() => {
        if (lastMessage !== null && typeof lastMessage.data === "string") {
            try {
                const latestData: Attendance[] = JSON.parse(lastMessage.data);
                setAttendances(latestData);
            } catch (e) {
                console.error("JSONに変換できません。: ", e);
            }
        }
    }, [lastMessage]);

    const connectionStatus = {
        [ReadyState.CONNECTING]: "Connecting",
        [ReadyState.OPEN]: "Open",
        [ReadyState.CLOSING]: "Closing",
        [ReadyState.CLOSED]: "Closed",
        [ReadyState.UNINSTANTIATED]: "Uninstantiated",
    }[readyState];

    return (
        <div>
            <h1>在室状況</h1>
            <p>{connectionStatus}</p>
            <table>
                <thead>
                    <tr>
                        <th>名前</th>
                        {STATUS_LIST.map((status) => (
                            <th key={status}>{status}</th>
                        ))}
                        <th>時刻</th>
                    </tr>
                </thead>
                <tbody>
                    {attendances.length > 0 ? (
                        attendances.map((attendance) => (
                            <tr key={attendance.id}>
                                <td>{attendance.name}</td>
                                    {STATUS_LIST.map((status) => (
                                        <td key={status}>
                                            {attendance.status === status ? '◯' : ''}
                                        </td>
                                    ))}
                                <td>{new Date(attendance.updated_at).toLocaleDateString('ja-JP')}</td>
                            </tr>
                        ))) : (
                            <tr>
                                <td colSpan={2 + STATUS_LIST.length}>
                                    データを待っています…
                                </td>
                            </tr>
                        )
                    }
                </tbody>
            </table>
        </div>
    )
}

export default AttendanceGrid;