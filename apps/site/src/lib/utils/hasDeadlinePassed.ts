export default function hasDeadlinePassed() {
	const pstDeadline = "2025-01-11T00:00:59";
	const utcOffset = "-08:00";

	const deadline = new Date(pstDeadline + utcOffset);
	const now = new Date();

	return now > deadline;
}
