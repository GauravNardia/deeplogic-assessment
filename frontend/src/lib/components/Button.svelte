<script lang="ts">
  import { string } from "zod";

  export let text: string;
  export let type: 'button' | 'submit' = 'submit';
</script>

<button
  type={type}
  class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition"
>
  {text}
</button>
