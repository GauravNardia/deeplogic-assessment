<script lang="ts">
  import { onMount } from 'svelte';
  import { Chart, BarController, BarElement, CategoryScale, LinearScale } from 'chart.js';
  import { token } from '$lib/store';
  import { get } from 'svelte/store';
    import { apiFetch } from '$lib/utils/api';

  Chart.register(BarController, BarElement, CategoryScale, LinearScale);

  let canvas: HTMLCanvasElement;

  onMount(async () => {
    const res = await apiFetch('/stats/issues-by-severity', {
      headers: { Authorization: `Bearer ${get(token)}` }
    });

    new Chart(canvas, {
      type: 'bar',
      data: {
        labels: ['LOW', 'MEDIUM', 'HIGH'],
        datasets: [{
          label: 'Open Issues',
          data: [res.LOW || 0, res.MEDIUM || 0, res.HIGH || 0],
          backgroundColor: ['#60a5fa', '#facc15', '#f87171']
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: {
              color: 'white'
            }
          }
        },
        scales: {
          x: {
            ticks: { color: 'white' },
            grid: { color: '#333' }
          },
          y: {
            beginAtZero: true,
            ticks: { color: 'white' },
            grid: { color: '#333' }
          }
        }
      }
    });
  });
</script>

<div class="bg-gray-900 p-6 rounded-xl shadow-xl border border-gray-700">
  <h2 class="text-xl font-semibold mb-4 text-white">Open Issues by Severity</h2>
  <canvas bind:this={canvas}></canvas>
</div>
