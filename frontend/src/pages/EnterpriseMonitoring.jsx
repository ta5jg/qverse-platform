import React from "react";
import { SystemHealthWidget } from "../components/widgets/SystemHealthWidget";
import { ActivityTimeline } from "../components/widgets/ActivityTimeline";

export default function EnterpriseMonitoring() {
  return (
    <div>
      <SystemHealthWidget />
      <ActivityTimeline />
    </div>
  );
}
