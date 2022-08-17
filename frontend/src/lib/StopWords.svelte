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
</script>

<div class="stop-words">
  {#each counterChecked as { active, text, size }}
    <span class="stop-word" class:active={active} on:click={handleClick({ active, text })} style="font-size={"2em"}">{text}</span>
  {/each}
</div>

<style>
  .stop-words {
    color: #888;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  .stop-word:hover {
    cursor: pointer;
    font-size: 1.1rem;
    color: rgb(166, 155, 91);
  }
  span {
    margin-right: 1em;
  }
  span.active {
    color: rgb(241, 109, 9);
  }
</style>