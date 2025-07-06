<script lang="ts">
  export let type = 'text';
  export let label: string;
  export let value: string;
  export let placeholder: string = '';
  export let error: string = '';
  export let onInput: (val: string) => void;    
  const inputId = `input-${Math.random().toString(36).substr(2, 9)}`;
</script>

<div class="flex flex-col gap-1">
  <label class="text-sm font-medium" for={inputId}>{label}</label>
  <input
    id={inputId}
    class="border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
    {type}
    {placeholder}
    value={value}
    on:input={(e) => onInput((e.target as HTMLInputElement)?.value ?? '')}
  />
  {#if error}
    <p class="text-sm text-red-500">{error}</p>
  {/if}
</div>