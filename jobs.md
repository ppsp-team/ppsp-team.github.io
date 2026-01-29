---
layout: default
title: Job Openings
permalink: /jobs/
---

{% include nav.html %}

<style>
  /* --- Masthead Styling --- */
  #jobs .masthead {
    height: 20vw;
    min-height: 200px;
    background-image: url("/assets/img/background-header.png");
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: flex-end;
    margin-bottom: 0;
  }
  
  #jobs .masthead-title h1 {
    font-size: 3.3rem;
    font-weight: 600;
    color: #f8f9fa;
    text-transform: uppercase;
    margin-bottom: 0; /* Align perfectly to bottom */
  }

  @media (max-width: 991px) {
    #jobs .masthead-title h1 {
      font-size: 2rem;
    }
  }

  /* --- Design System Refinement --- */
  :root {
    --job-primary: #0f6cb6;
    --job-bg-light: #f8fbff;
    --job-phd: #4a90e2;
    --job-postdoc: #f5a623;
    --job-ra: #7ed321;
    --job-intern: #d0021b;
    --job-shadow: 0 4px 20px rgba(15, 108, 182, 0.08);
    --job-shadow-hover: 0 12px 30px rgba(15, 108, 182, 0.15);
  }

  /* Page Structure */
  .jobs-section {
    background-color: var(--job-bg-light);
    padding: 60px 0;
  }

  .section-title-container {
    margin-bottom: 50px;
  }

  .section-heading {
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #2c3e50;
  }

  /* Sidebar Styling */
  .job-sidebar {
    background: white;
    border-radius: 16px;
    padding: 25px;
    position: sticky;
    top: 110px;
    box-shadow: var(--job-shadow);
    border: 1px solid rgba(15, 108, 182, 0.05);
  }

  .sidebar-title {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #95a5a6;
    margin-bottom: 15px;
    display: block;
    font-weight: 600;
  }

  .filter-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .filter-pill {
    border: 1px solid #e0e6ed;
    background: transparent;
    color: #7f8c8d;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .filter-pill:hover {
    border-color: var(--job-primary);
    color: var(--job-primary);
    background: rgba(15, 108, 182, 0.05);
  }

  .filter-pill.active {
    background: var(--job-primary);
    border-color: var(--job-primary);
    color: white;
    box-shadow: 0 4px 12px rgba(15, 108, 182, 0.3);
  }

  /* Job Card Redesign */
  .job-card {
    background: white;
    border-radius: 16px;
    padding: 30px;
    box-shadow: var(--job-shadow);
    border: 1px solid rgba(15, 108, 182, 0.05);
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    height: 100%;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
  }

  .job-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--job-primary);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .job-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--job-shadow-hover);
  }

  .job-card:hover::before {
    opacity: 1;
  }

  .job-card-archived {
    background: #fcfdfe;
    filter: grayscale(0.5);
    opacity: 0.8;
  }

  .job-icon-box {
    width: 45px;
    height: 45px;
    background: rgba(15, 108, 182, 0.1);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    color: var(--job-primary);
    font-size: 1.2rem;
  }

  .job-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #2c3e50;
    line-height: 1.3;
    margin-bottom: 12px;
  }

  .job-meta-tags {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  .job-type-badge {
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .badge-phd { background: #e3f2fd; color: #1e88e5; }
  .badge-postdoc { background: #fff8e1; color: #ffa000; }
  .badge-ra { background: #e8f5e9; color: #43a047; }
  .badge-internship { background: #fbe9e7; color: #d84315; }

  .job-status-indicator {
    display: inline-flex;
    align-items: center;
    font-size: 0.8rem;
    font-weight: 500;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
  }

  .status-open .status-dot { background: #2ecc71; box-shadow: 0 0 8px #2ecc71; }
  .status-closed .status-dot { background: #95a5a6; }

  .job-excerpt {
    color: #7f8c8d;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 25px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .job-card-action {
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    border-top: 1px solid #f0f3f5;
  }

  .deadline-info {
    font-size: 0.8rem;
    color: #95a5a6;
    display: flex;
    align-items: center;
  }

  .deadline-info i { margin-right: 5px; }

  /* Modal Enhancements */
  .modal-content {
    border: none;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  }

  .modal-header {
    background: #f8fbff;
    border-bottom: 1px solid #edf2f7;
    padding: 30px;
    border-radius: 20px 20px 0 0;
  }

  .modal-title {
    font-weight: 800;
    color: #2c3e50;
  }

  .modal-body {
    padding: 40px;
  }

  .job-info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    background: #f8fbff;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 30px;
  }

  .info-item label {
    display: block;
    font-size: 0.75rem;
    color: #95a5a6;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 5px;
  }

  .info-item span {
    font-weight: 600;
    color: #2c3e50;
  }

  .section-subtitle {
    font-size: 1rem;
    font-weight: 700;
    color: var(--job-primary);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
  }

  .section-subtitle::after {
    content: '';
    flex-grow: 1;
    height: 1px;
    background: #edf2f7;
    margin-left: 15px;
  }

  .job-rich-text {
    line-height: 1.8;
    color: #4a5568;
  }

  .job-rich-text ul {
    padding-left: 20px;
  }

  .job-rich-text li {
    margin-bottom: 10px;
  }

  .modal-footer {
    padding: 25px 40px;
    border-top: 1px solid #edf2f7;
  }

  /* Responsive Fixes */
  @media (max-width: 991px) {
    .job-sidebar {
      position: relative;
      top: 0;
      margin-bottom: 40px;
    }
  }
</style>

<!-- Main Content -->
<section id="jobs" class="page-section" style="padding: 20px 0;">
  
  {% include header.html %}

  <div class="container-fluid bg-light py-5">
    <div class="container">
      <div class="row">
      
      <!-- Filters Sidebar -->
      <aside class="col-lg-3">
        <div class="job-sidebar">
          
          <div class="sidebar-section">
            <h6 class="sidebar-title">{% t jobs.current_status %}</h6>
            <div class="filter-group">
              <button class="filter-pill active" data-filter="open" onclick="toggleStatusFilter(this, 'open')">{% t jobs.open %}</button>
              <button class="filter-pill" data-filter="all" onclick="toggleStatusFilter(this, 'all')">{% t jobs.all_roles %}</button>
              <button class="filter-pill" data-filter="closed" onclick="toggleStatusFilter(this, 'closed')">{% t jobs.archived %}</button>
            </div>
          </div>

          <div class="sidebar-section">
            <h6 class="sidebar-title">{% t jobs.position_category %}</h6>
            <div class="filter-group">
              <button class="filter-pill active" data-filter="all" onclick="toggleTypeFilter(this)">{% t jobs.all_roles %}</button>
              <button class="filter-pill" data-filter="phd" onclick="toggleTypeFilter(this)">{% t jobs.phd %}</button>
              <button class="filter-pill" data-filter="postdoc" onclick="toggleTypeFilter(this)">{% t jobs.postdoc %}</button>
              <button class="filter-pill" data-filter="research assistant" onclick="toggleTypeFilter(this)">{% t jobs.assistant %}</button>
              <button class="filter-pill" data-filter="internship" onclick="toggleTypeFilter(this)">{% t jobs.internship %}</button>
            </div>
          </div>

        </div>
      </aside>

      <!-- Jobs Feed -->
      <main class="col-lg-9">
        <div class="row" id="jobsContainer">
          {% assign jobs = site.data.jobs.jobs %}
          {% for job in jobs %}
          {% if job.active %}
           <div class="col-xl-6 col-lg-12 mb-4 job-card-wrapper" 
               data-status="{% if job.active %}open{% else %}closed{% endif %}" 
               data-type="{{ job.type | downcase }}"
               data-id="{{ job.id }}">
            
            <div class="job-card {% if job.status == 'closed' %}job-card-archived{% endif %}">
              <div class="job-icon-box">
                {% if job.type == 'PhD' %}<i class="fas fa-graduation-cap"></i>
                {% elsif job.type == 'Postdoc' %}<i class="fas fa-microscope"></i>
                {% elsif job.type == 'Research Assistant' %}<i class="fas fa-clipboard-list"></i>
                {% elsif job.type == 'Internship' %}<i class="fas fa-lightbulb"></i>
                {% else %}<i class="fas fa-briefcase"></i>{% endif %}
              </div>

              {% if site.lang == 'fr' %}
                <h4 class="job-title">{{ job.title.fr }}</h4>
                {% if job.subtitle %}<p class="text-muted mb-2" style="font-weight: 500;">{{ job.subtitle.fr }}</p>{% endif %}
              {% else %}
                <h4 class="job-title">{{ job.title.en }}</h4>
                {% if job.subtitle %}<p class="text-muted mb-2" style="font-weight: 500;">{{ job.subtitle.en }}</p>{% endif %}
              {% endif %}

              <div class="job-meta-tags">
                {% assign job_type_key = job.type | downcase | replace: ' ', '_' %}
                <span class="job-type-badge badge-{{ job.type | downcase | replace: ' ', '-' }}">
                  {% if job_type_key == 'research_assistant' %}
                    {{ site.translations[site.lang].jobs.assistant }}
                  {% else %}
                    {{ site.translations[site.lang].jobs[job_type_key] }}
                  {% endif %}
                </span>
                <div class="job-status-indicator status-{% if job.active %}open{% else %}closed{% endif %}">
                  <span class="status-dot"></span>
                  {% if job.active %}{% t jobs.open %}{% else %}{% t jobs.closed %}{% endif %}
                </div>
              </div>

              {% if job.mission %}
                {% if site.lang == 'fr' %}
                  <p class="job-excerpt">{{ job.mission.fr | strip_html | truncate: 200 }}</p>
                {% else %}
                  <p class="job-excerpt">{{ job.mission.en | strip_html | truncate: 200 }}</p>
                {% endif %}
              {% endif %}

              <div class="job-card-action">
                <span class="deadline-info">
                  {% if site.lang == 'fr' %}
                    <i class="far fa-calendar-alt"></i> {{ job.start.fr }}
                  {% else %}
                    <i class="far fa-calendar-alt"></i> {{ job.start.en }}
                  {% endif %}
                </span>
                <button class="btn btn-primary btn-sm rounded-pill px-4" 
                        onclick="openJobModal('{{ job.id }}')" 
                        {% unless job.active %}disabled{% endunless %}>
                  {% if job.active %}{% if site.lang == 'fr' %}Voir l'offre{% else %}View offer{% endif %}{% else %}{% if site.lang == 'fr' %}Pourvu{% else %}Filled{% endif %}{% endif %}
                </button>
              </div>
            </div>
          </div>
          {% endif %}
          {% endfor %}
        </div>
        
        <div id="noResult" class="text-center py-5" style="display: none;">
          <i class="fas fa-search-minus fa-3x text-muted mb-3"></i>
          <p class="text-muted">No positions currently match your criteria.</p>
        </div>
      </main>
      
    </div>
  </div>
</div>
</section>

<!-- Improved Modals -->
{% for job in site.data.jobs.jobs %}
{% if job.active %}
<div class="modal fade" id="modal-{{ job.id }}" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
    <div class="modal-content">
      <div class="modal-header d-flex flex-column align-items-start">
        <div class="d-flex justify-content-between w-100">
          {% if site.lang == 'fr' %}
            <h4 class="modal-title">{{ job.title.fr }}</h4>
          {% else %}
            <h4 class="modal-title">{{ job.title.en }}</h4>
          {% endif %}
          <button type="button" class="close" data-dismiss="modal">&times;</button>
        </div>
        <div class="job-meta-tags mt-2">
          <span class="job-type-badge badge-{{ job.type | downcase | replace: ' ', '-' }}">{{ job.type | capitalize }}</span>
          <div class="job-status-indicator status-{% if job.active %}open{% else %}closed{% endif %}">
            <span class="status-dot"></span>
            {% if job.active %}{% if site.lang == 'fr' %}Ouvert{% else %}Open{% endif %}{% else %}{% if site.lang == 'fr' %}Fermé{% else %}Closed{% endif %}{% endif %}
          </div>
        </div>
      </div>
      
      <div class="modal-body">
        <div class="job-info-grid">
          {% if site.lang == 'fr' %}
            <div class="info-item"><label>Lieu</label><span>{{ job.location.fr }}</span></div>
            <div class="info-item"><label>Durée</label><span>{{ job.duration.fr }}</span></div>
            <div class="info-item"><label>Début</label><span>{{ job.start.fr }}</span></div>
            {% if job.onsite %}<div class="info-item"><label>Présentiel</label><span>{{ job.onsite.fr }}</span></div>{% endif %}
          {% else %}
            <div class="info-item"><label>Location</label><span>{{ job.location.en }}</span></div>
            <div class="info-item"><label>Duration</label><span>{{ job.duration.en }}</span></div>
            <div class="info-item"><label>Start</label><span>{{ job.start.en }}</span></div>
            {% if job.onsite %}<div class="info-item"><label>On-site</label><span>{{ job.onsite.en }}</span></div>{% endif %}
          {% endif %}
        </div>

        {% if job.project %}
        <div class="mb-5">
          <h6 class="section-subtitle"><i class="fas fa-project-diagram mr-2"></i> {% if site.lang == 'fr' %}Projet{% else %}Project{% endif %}</h6>
          {% if site.lang == 'fr' %}
            <div class="job-rich-text">{{ job.project.fr | markdownify }}</div>
          {% else %}
            <div class="job-rich-text">{{ job.project.en | markdownify }}</div>
          {% endif %}
        </div>
        {% endif %}

        {% if job.mission %}
        <div class="mb-5">
          <h6 class="section-subtitle"><i class="fas fa-bullseye mr-2"></i> {% if site.lang == 'fr' %}Mission{% else %}Mission{% endif %}</h6>
          {% if site.lang == 'fr' %}
            <div class="job-rich-text">{{ job.mission.fr | markdownify }}</div>
          {% else %}
            <div class="job-rich-text">{{ job.mission.en | markdownify }}</div>
          {% endif %}
        </div>
        {% endif %}

        {% if job.tasks %}
        <div class="mb-5">
          <h6 class="section-subtitle"><i class="fas fa-tasks mr-2"></i> {% if site.lang == 'fr' %}Tâches{% else %}Tasks{% endif %}</h6>
          <div class="job-rich-text">
            {% if site.lang == 'fr' %}
              <ul>{% for task in job.tasks.fr %}<li>{{ task }}</li>{% endfor %}</ul>
            {% else %}
              <ul>{% for task in job.tasks.en %}<li>{{ task }}</li>{% endfor %}</ul>
            {% endif %}
          </div>
        </div>
        {% endif %}

        {% if job.profile %}
        <div class="mb-5">
          <h6 class="section-subtitle"><i class="fas fa-user-circle mr-2"></i> {% if site.lang == 'fr' %}Profil Recherché{% else %}Profile{% endif %}</h6>
          <div class="job-rich-text">
            {% if site.lang == 'fr' %}{{ job.profile.fr | markdownify }}{% else %}{{ job.profile.en | markdownify }}{% endif %}
          </div>
        </div>
        {% endif %}

        {% if job.skills %}
        <div class="mb-5">
          <h6 class="section-subtitle"><i class="fas fa-graduation-cap mr-2"></i> {% if site.lang == 'fr' %}Compétences Développées{% else %}Skills You Will Develop{% endif %}</h6>
          <div class="job-rich-text">
            {% if site.lang == 'fr' %}{{ job.skills.fr | markdownify }}{% else %}{{ job.skills.en | markdownify }}{% endif %}
          </div>
        </div>
        {% endif %}

        {% if job.supervision %}
        <div class="mb-5">
          <h6 class="section-subtitle"><i class="fas fa-users mr-2"></i> {% if site.lang == 'fr' %}Encadrement{% else %}Supervision{% endif %}</h6>
          <div class="job-rich-text">
            {% if site.lang == 'fr' %}{{ job.supervision.fr | markdownify }}{% else %}{{ job.supervision.en | markdownify }}{% endif %}
          </div>
        </div>
        {% endif %}

        {% if job.process %}
        <div class="mb-5">
          <h6 class="section-subtitle"><i class="fas fa-file-alt mr-2"></i> {% if site.lang == 'fr' %}Procédure de Recrutement{% else %}Application Process{% endif %}</h6>
          <div class="job-rich-text">
            {% if site.lang == 'fr' %}{{ job.process.fr | markdownify }}{% else %}{{ job.process.en | markdownify }}{% endif %}
          </div>
        </div>
        {% endif %}
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-light rounded-pill px-4" data-dismiss="modal">{% if site.lang == 'fr' %}Fermer{% else %}Close{% endif %}</button>
        {% if job.active %}
        <a href="mailto:{{ job.contact }}" class="btn btn-primary rounded-pill px-5 shadow">{% if site.lang == 'fr' %}Postuler{% else %}Apply{% endif %}</a>
        {% endif %}
      </div>
    </div>
  </div>
</div>
{% endif %}
{% endfor %}

<script>
  let currentStatus = 'open';
  let currentType = 'all';

  function toggleStatusFilter(btn, s) {
    btn.closest('.filter-group').querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentStatus = s;
    applyFilters();
  }

  function toggleTypeFilter(btn) {
    btn.closest('.filter-group').querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentType = btn.dataset.filter;
    applyFilters();
  }

  function applyFilters() {
    const cards = document.querySelectorAll('.job-card-wrapper');
    let count = 0;

    cards.forEach(c => {
      const s = c.dataset.status;
      const t = c.dataset.type;
      
      const sMatch = (currentStatus === 'all' || s === currentStatus);
      const tMatch = (currentType === 'all' || t === currentType);

      if (sMatch && tMatch) {
        c.style.display = '';
        count++;
      } else {
        c.style.display = 'none';
      }
    });
    document.getElementById('noResult').style.display = count === 0 ? 'block' : 'none';
  }

  function openJobModal(id) { $('#modal-' + id).modal('show'); }

  document.addEventListener('DOMContentLoaded', applyFilters);
</script>
