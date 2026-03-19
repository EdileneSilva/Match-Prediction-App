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
                v-model="profileData.name"
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
export default {
  name: "ProfileView",
  data() {
    return {
      isSaving: false,
      profileData: {
        name: "John Doe",
        email: "adresse@email.com",
        password: "",
        photo: null,
      },
    };
  },
  methods: {
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

      // Simulate API call
      setTimeout(() => {
        this.isSaving = false;
        alert("Profil mis à jour avec succès!");
      }, 1500);
    },

    deleteAccount() {
      if (
        confirm(
          "Êtes-vous sûr de vouloir supprimer votre compte? Cette action est irréversible.",
        )
      ) {
        // Simulate account deletion
        alert("Compte supprimé avec succès");
        this.$router.push("/login");
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

/* Navigation (same as other views) */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

.nav-menu {
  display: flex;
  gap: 2rem;
}

.nav-item {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  color: white;
  background: rgba(255, 255, 255, 0.2);
}

.nav-item.exit {
  background: rgba(255, 67, 54, 0.3);
  color: #ff4336;
}

.nav-item.exit:hover {
  background: rgba(255, 67, 54, 0.5);
}

/* Main Content */
.main-content {
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.profile-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.page-title {
  margin: 0 0 2rem 0;
  color: #333;
  font-size: 2rem;
  font-weight: 600;
  text-align: center;
}

/* Profile Form */
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.photo-section {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.photo-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #667eea;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

/* Form Fields */
.form-fields {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #555;
  font-size: 0.95rem;
}

.form-input {
  padding: 0.875rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fafafa;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.photo-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
}

.photo-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.save-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.delete-btn {
  width: 100%;
  background: transparent;
  color: #dc3545;
  border: 1px solid #dc3545;
  padding: 0.875rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-btn:hover {
  background: #dc3545;
  color: white;
}

.logo-img {
  height: 1.5rem;
  width: auto;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }

  .main-content {
    padding: 1rem;
  }

  .profile-container {
    padding: 1.5rem;
  }

  .photo-section {
    flex-direction: column;
    text-align: center;
  }

  .page-title {
    font-size: 1.5rem;
  }
}
</style>
