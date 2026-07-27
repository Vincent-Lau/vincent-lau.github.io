```{=html}
<div class="research-list list">

<% for (const item of items) { %>
  <article class="research-item" <%= metadataAttrs(item) %>>

    <h3 class="research-title listing-title">
      <%= item.title %>
    </h3>

    <% if (item.subtitle) { %>
      <div class="research-subtitle listing-subtitle">
        <%= item.subtitle %>
      </div>
    <% } %>

    <div class="research-details">

      <% if (item.authors) { %>
        <% const authorText = Array.isArray(item.authors)
          ? item.authors.join(", ")
          : item.authors; %>
        <div class="research-field research-authors listing-authors">
          <span class="research-label">Authors:</span>
          <span class="research-value"><%= authorText %></span>
        </div>
      <% } %>

      <% if (item.status) { %>
        <div class="research-field research-status">
          <span class="research-label">Status:</span>
          <span class="research-value"><%= item.status %></span>
        </div>
      <% } %>

      <% if (item.journal) { %>
        <div class="research-field research-journal">
          <span class="research-label">Journal:</span>
          <span class="research-value"><%= item.journal %></span>
        </div>
      <% } %>

      <% if (item.year) { %>
        <div class="research-field research-year">
          <span class="research-label">Year:</span>
          <span class="research-value"><%= item.year %></span>
        </div>
      <% } %>

      <% if (item.doi) { %>
        <div class="research-field research-doi">
          <span class="research-label">DOI:</span>
          <span class="research-value">
            <a href="https://doi.org/<%= item.doi %>"
              target="_blank"
              rel="noopener noreferrer">
              <%= item.doi %>
            </a>
          </span>
        </div>
      <% } %>

      <% if (item.pdf) { %>
        <div class="research-links">
          <a href="<%= item.pdf %>" target="_blank" rel="noopener noreferrer">
            PDF
          </a>
        </div>
      <% } %>

    </div>

  </article>
<% } %>

</div>
```