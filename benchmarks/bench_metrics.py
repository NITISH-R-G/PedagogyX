import timeit


def baseline_loop(segments):
    teacher_dur = 0.0
    total_dur = 0.0
    for i, seg in enumerate(segments):
        dur = max(0.0, float(seg.get("end", 0)) - float(seg.get("start", 0)))
        total_dur += dur
        if i % 2 == 0:
            teacher_dur += dur
    return teacher_dur, total_dur


def optimized_loop(segments):
    teacher_dur = 0.0
    total_dur = 0.0
    is_teacher = True
    for seg in segments:
        try:
            start = seg["start"]
            end = seg["end"]
        except (KeyError, TypeError):
            start = seg.get("start", 0) if isinstance(seg, dict) else 0
            end = seg.get("end", 0) if isinstance(seg, dict) else 0
        dur = float(end) - float(start)
        if dur < 0.0:
            dur = 0.0
        total_dur += dur
        if is_teacher:
            teacher_dur += dur
        is_teacher = not is_teacher
    return teacher_dur, total_dur


def run_benchmark():
    segments = [
        {"start": float(i), "end": float(i + 1.5), "text": f"segment {i}"} for i in range(1000)
    ]
    iterations = 10000

    time_baseline = timeit.timeit(lambda: baseline_loop(segments), number=iterations)
    time_optimized = timeit.timeit(lambda: optimized_loop(segments), number=iterations)

    speedup = time_baseline / time_optimized
    reduction = (1.0 - time_optimized / time_baseline) * 100.0

    print(f"Baseline loop time ({iterations} iter): {time_baseline:.4f}s")
    print(f"Optimized loop time ({iterations} iter): {time_optimized:.4f}s")
    print(f"Speedup: {speedup:.2f}x ({reduction:.1f}% reduction in execution time)")


if __name__ == "__main__":
    run_benchmark()
