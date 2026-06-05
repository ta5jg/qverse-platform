"""Capacity Engine"""



def calculate_capacity(self, state: SystemState) -> CapacityReport:
        cpu_count = state.hardware.get('cpu_count') or 1
        ram_bytes = state.ram.get('total_bytes') or 0
        ram_gb = ram_bytes / (1024 ** 3)

        estimated = max(1, int(min(cpu_count * 4, ram_gb * 2)))

        if estimated >= 50:
            profile = 'enterprise'
        elif estimated >= 20:
            profile = 'production'
        elif estimated >= 5:
            profile = 'small_business'
        else:
            profile = 'development'

        return CapacityReport(
            max_agents=estimated,
            profile=profile,
        )

def estimate_cost(self, state: SystemState) -> CostEstimate:
        agents = max(1, len(state.projects))
        estimated = round(agents * 5.0, 2)

        if estimated < 25:
            profile = 'development'
        elif estimated < 100:
            profile = 'business'
        else:
            profile = 'enterprise'

        return CostEstimate(
            monthly_usd=estimated,
            profile=profile,
        )

def benchmark_system(self, state: SystemState) -> BenchmarkReport:
        cpu_score = min(100, (state.hardware.get('cpu_count') or 1) * 8)

        ram_gb = (state.ram.get('total_bytes') or 0) / (1024 ** 3)
        ram_score = min(100, int(ram_gb * 4))

        disk_free = state.disk.get('free', 0)
        disk_score = 100 if disk_free > 100 * 1024**3 else 70

        overall = int((cpu_score + ram_score + disk_score) / 3)

        return BenchmarkReport(
            cpu_score=cpu_score,
            ram_score=ram_score,
            disk_score=disk_score,
            overall_score=overall,
        )