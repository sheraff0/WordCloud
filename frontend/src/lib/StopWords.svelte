<script>
  import { upload } from './store'
// Calculated values
  $: counterChecked = $upload.counterChecked || []
// Handlers
  const handleClick = ({ active, text }) => e => upload[
    active
    ? "removeStopword"
    : "addStopword"
  ](text)
  const handleReset = e => upload.resetStopwords()
</script>

{#if counterChecked.length > 0}
  <div class="stop-words">
    <span class="button-reset" on:click={handleReset}>СБРОСИТЬ</span>
    {#each counterChecked as { active, text, size }}
      <span class="stop-word" class:active={active} on:click={handleClick({ active, text })} style="font-size={"2em"}">{text}</span>
    {/each}
  </div>
{/if}

<style>
  .stop-words {
    color: #888;
    padding: 1em 2em;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  span {
    margin-right: 1em;
  }
  span.active {
    color: rgb(241, 109, 9);
  }
  span.button-reset {
    color: #aaa;
    background-color: #111;
    padding: 0 1em;
    border-radius: 10%;
  }
  span:hover {
    cursor: pointer;
    font-size: 1.03rem;
    color: rgb(166, 155, 91);
  }
</style>