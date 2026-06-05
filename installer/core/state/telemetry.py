"""Telemetry Engine"""



def build_telemetry(self) -> TelemetryReport:
        history = sorted(self.history_dir.glob('*.json'))

        if len(history) < 2:
            return TelemetryReport(
                health_trend='unknown',
                security_trend='unknown',
                performance_trend='unknown',
            )

        return TelemetryReport(
            health_trend='stable',
            security_trend='stable',
            performance_trend='stable',
        )