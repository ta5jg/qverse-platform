import React from "react";
import { RuntimeWidget } from "../components/widgets/RuntimeWidget";
import { ServiceStatusWidget } from "../components/widgets/ServiceStatusWidget";
import { TelemetryWidget } from "../components/widgets/TelemetryWidget";

export default function EnterpriseOperations() {
  return (
    <div>
      <RuntimeWidget />
      <ServiceStatusWidget />
      <TelemetryWidget />
    </div>
  );
}
