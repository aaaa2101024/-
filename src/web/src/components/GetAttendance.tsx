import { useEffect, useState } from "react";
import useWebSocket from "react-use-websocket";
import type { Attendance } from "../type/Attendance";
import GridTable from "./GridTable";
import "./css/GetAttendance.css";

const API_URL = "http://localhost:8000/attendance";
const WEBSOCKET_URL = "";
const STATUS_LIST: string[] = ["在室", "休憩中", "退室"];

const GetAttendance = () => {
    const [attendances, setAttendances] = useState<Attendance[]>([]);
    const [error, setError] = useState<string>("");
    const { lastMessage } = useWebSocket(WEBSOCKET_URL);

    // 起動した際にデータを取得
    useEffect(() => {
        const firstFetch = async () => {
            const response = await fetch(API_URL);

            if (!response) {
                console.error("データの取得に失敗しました。");
                setError("データの取得に失敗しました。");
            }

            const data = await response.json();
            setAttendances(data);
        }

        firstFetch();
    }, []);

    // データベースが更新される度にデータを更新
    useEffect(() => {
        if (lastMessage !== null && typeof lastMessage.data === "string") {
            try {
                const latestData: Attendance[] = JSON.parse(lastMessage.data);
                setAttendances(latestData);
            } catch (e) {
                console.error("JSONを変換できません。: ", e);
            }
        }
    }, [lastMessage]);

    return (
        <div className="get-attendance-container">
            <h1 className="get-attendance-title">在室状況</h1>
            {error && (
                <p className="get-attendance-error">{error}</p>
            )}
            <GridTable attendances={attendances} STATUS_LIST={STATUS_LIST} />
        </div>
    )
}

export default GetAttendance;