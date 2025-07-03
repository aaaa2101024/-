import type { Attendance } from "../type/Attendance";
import "./css/GridTable.css";

type TableProps = {
    attendances: Attendance[],
    STATUS_LIST: string[],
};

const GridTable = ({ attendances, STATUS_LIST }: TableProps) => {
    return (
        <div className="table-container">
            <table className="cool-table">
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
                                        {attendance.status === status ? <span className="status-circle">◯</span> : ""}
                                    </td>
                                ))}
                                <td className="time">{new Date(attendance.updated_at).toLocaleDateString("ja-JP")}</td>
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

export default GridTable;