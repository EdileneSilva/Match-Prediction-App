<template>
  <div class="dashboard">
    <!-- Main Content -->
    <main class="main-content">
      <div class="profile-container">
        <h1 class="page-title">Mon Profil</h1>

        <!-- Profile Form -->
        <div class="profile-form">
          <!-- Photo Section -->
          <div class="photo-section">
            <div class="photo-placeholder">
              <img
                v-if="profileData.photo"
                :src="profileData.photo"
                alt="Photo"
                class="profile-photo"
              />
              <div v-else class="default-avatar">
                <svg
                  width="80"
                  height="80"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12Z"
                    fill="#999"
                  />
                  <path
                    d="M12 14C7.59 14 4 17.59 4 22H20C20 17.59 16.41 14 12 14Z"
                    fill="#999"
                  />
                </svg>
              </div>
            </div>
            <div class="form-group">
              <label for="photo">Photo</label>
              <input
                type="file"
                id="photo"
                @change="handlePhotoChange"
                accept="image/*"
                class="photo-input"
              />
            </div>
          </div>

          <!-- Form Fields -->
          <div class="form-fields">
            <div class="form-group">
              <label for="name">Nom</label>
              <input
                type="text"
                id="name"
                v-model="profileData.username"
                placeholder="Votre nom"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label for="email">Email</label>
              <input
                type="email"
                id="email"
                v-model="profileData.email"
                placeholder="adresse@email.com"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label for="password">Mot de passe</label>
              <input
                type="password"
                id="password"
                v-model="profileData.password"
                placeholder="••••••••"
                class="form-input"
              />
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <button class="save-btn" @click="saveProfile" :disabled="isSaving">
              {{ isSaving ? "Enregistrement..." : "Enregistrer modifications" }}
            </button>

            <button class="delete-btn" @click="deleteAccount">
              Supprimer mon compte
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { apiClient } from "@/api/client";
import { gsap } from "gsap";

export default {
  name: "ProfileView",
  data() {
    return {
      isSaving: false,
      profileData: {
        username: "",
        email: "",
        password: "",
        photo: null,
      },
    };
  },
  async mounted() {
    await this.fetchProfile();
    
    this.$nextTick(() => {
      // Entrance container animation
      gsap.fromTo('.profile-container',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }
      )
      
      // Stagger elements
      gsap.fromTo(['.photo-section', '.form-group', '.action-buttons'],
        { opacity: 0, x: -20 },
        { opacity: 1, x: 0, duration: 0.5, stagger: 0.1, ease: 'power2.out', delay: 0.2 }
      )
    })
  },
  methods: {
    async fetchProfile() {
      try {
        const data = await apiClient.get("/auth/me");
        this.profileData.username = data.username;
        this.profileData.email = data.email;
      } catch (err) {
        console.error("Erreur lors de la récupération du profil", err);
      }
    },
    handlePhotoChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.profileData.photo = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    async saveProfile() {
      this.isSaving = true;
      try {
        await apiClient.put("/auth/me", {
          username: this.profileData.username,
          email: this.profileData.email,
        });
        alert("Profil mis à jour avec succès!");
      } catch (err) {
        alert("Erreur: " + (err.message || "Inconnue"));
      } finally {
        this.isSaving = false;
      }
    },

    async deleteAccount() {
      if (
        confirm(
          "Êtes-vous sûr de vouloir supprimer votre compte? Cette action est irréversible.",
        )
      ) {
        try {
          await apiClient.delete("/auth/me");
          alert("Compte supprimé avec succès");
          localStorage.removeItem("token");
          this.$router.push("/login");
        } catch (err) {
          alert("Erreur lors de la suppression: " + err.message);
        }
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-image: linear-gradient(rgba(10, 10, 26, 0.4), rgba(10, 10, 26, 0.6)), url("@/assets/stadium1.png");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  font-family: "Inter", sans-serif;
  color: var(--text-primary);
}

/* Main Content */
.main-content {
  padding: 100px 2rem 2rem;
  max-width: 650px;
  margin: 0 auto;
}

.profile-container {
  background: var(--glass-bg);
  border-radius: 28px;
  padding: 3.5rem;
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
}

.page-title {
  margin: 0 0 3rem 0;
  color: var(--text-primary);
  font-size: 2.5rem;
  font-weight: 800;
  text-align: center;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -1px;
}

/* Profile Form */
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.photo-section {
  display: flex;
  align-items: center;
  gap: 2.5rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 20px;
  border: 1px solid var(--glass-border);
}

.photo-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid var(--accent-secondary);
  background: var(--glass-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.profile-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-avatar svg path {
  fill: var(--accent-secondary);
  opacity: 0.6;
}

/* Form Fields */
.form-fields {
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.form-group label {
  font-weight: 700;
  color: var(--text-secondary);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.form-input {
  padding: 1.1rem 1.4rem;
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-primary);
  font-weight: 500;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.form-input:focus {
  outline: none;
  border-color: var(--accent-secondary);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}

.photo-input {
  padding: 0.6rem;
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  font-size: 0.85rem;
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.02);
  cursor: pointer;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--glass-border);
}

.save-btn {
  width: 100%;
  background: var(--accent-gradient);
  color: white;
  border: none;
  padding: 1.2rem;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(224, 38, 255, 0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(224, 38, 255, 0.5);
  filter: brightness(1.1);
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #334155;
  box-shadow: none;
}

.delete-btn {
  width: 100%;
  background: transparent;
  color: #f87171;
  border: 1px solid rgba(248, 113, 113, 0.3);
  padding: 1rem;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-btn:hover {
  background: rgba(248, 113, 113, 0.05);
  border-color: #f87171;
  box-shadow: 0 0 20px rgba(248, 113, 113, 0.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    padding: 100px 1rem 2rem;
  }

  .profile-container {
    padding: 2rem;
  }

  .photo-section {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
}

</style>
