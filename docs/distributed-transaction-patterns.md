
# Distributed transaction patterns

Patterns for managing distributed transactions with compensating actions and coordination across multiple services.

<div class="pattern-grid">
<div class="pattern-tile">
<a href="saga-pattern">
<div class="pattern-tile-header">
<img src="/images/saga-icon.png" alt="Saga Pattern">
<span>Saga Pattern</span>
</div>
<p>Manages distributed transactions with compensating actions. Each step has a compensation that undoes its effects if subsequent steps fail.</p>
</a>
</div>

<div class="pattern-tile">
<a href="early-return">
<div class="pattern-tile-header">
<img src="/images/early-return-icon.png" alt="Early Return">
<span>Early Return</span>
</div>
<p>Synchronous initialization with asynchronous completion. Returns results immediately while processing continues in the background.</p>
</a>
</div>
</div>
