"use client";

import { useContext } from "react";

import Container from "@cloudscape-design/components/container";
import ContentLayout from "@cloudscape-design/components/content-layout";
import SpaceBetween from "@cloudscape-design/components/space-between";

import { isApplicationManager } from "@/lib/admin/authorization";
import UserContext from "@/lib/admin/UserContext";

import ApplicantSummary from "./components/ApplicantSummary";
import HackerCount from "./components/HackerCount";

function AdminDashboard() {
	const { roles } = useContext(UserContext);

	return (
		<ContentLayout>
			<SpaceBetween size="l">
				<Container>Admin Dashboard</Container>
				{isApplicationManager(roles) && <ApplicantSummary />}
				<HackerCount />
			</SpaceBetween>
		</ContentLayout>
	);
}

export default AdminDashboard;
