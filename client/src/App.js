import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useNavigate,
  useParams,
} from "react-router-dom";
import axios from "axios";

// API Configuration
const API_BASE_URL = "http://127.0.0.1:8000/api";

// Set up axios defaults
axios.defaults.baseURL = API_BASE_URL;

// Auth Context
const AuthContext = React.createContext();

// Auth Provider Component
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      // Verify token and get user info
      axios
        .get("/auth/")
        .then((response) => {
          setUser({ username: "user" }); // Simple user info
          setIsLoading(false);
        })
        .catch(() => {
          localStorage.removeItem("token");
          setToken(null);
          setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await axios.post("/token/", { username, password });
      const { access, refresh } = response.data;
      localStorage.setItem("token", access);
      localStorage.setItem("refresh", refresh);
      setToken(access);
      axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;
      setUser({ username });
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || "Login failed",
      };
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await axios.post("/register/", {
        username,
        email,
        password,
      });
      const { access, refresh } = response.data;
      localStorage.setItem("token", access);
      localStorage.setItem("refresh", refresh);
      setToken(access);
      axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;
      setUser({ username });
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error:
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Registration failed",
      };
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common["Authorization"];
  };

  return (
    <AuthContext.Provider
      value={{ user, token, login, register, logout, isLoading }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use auth context
function useAuth() {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

// Navigation Component
function Navigation() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="container">
        <h1>
          <Link to="/">📝 Blog App</Link>
        </h1>
        <div>
          {user ? (
            <>
              <span
                style={{
                  color: "var(--text-primary)",
                  marginRight: "1rem",
                  fontWeight: "600",
                  background: "var(--primary-light)",
                  padding: "0.5rem 1rem",
                  borderRadius: "var(--radius-md)",
                  fontSize: "0.9rem",
                }}
              >
                👋 Welcome, {user.username}!
              </span>
              <Link to="/articles/new">✍️ New Article</Link>
              <button
                onClick={handleLogout}
                className="btn btn-secondary"
                style={{ marginLeft: "1rem" }}
              >
                🚪 Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login">🔑 Login</Link>
              <Link to="/register">📝 Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

// Home Page Component
function HomePage() {
  const [articles, setArticles] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async (query = "") => {
    try {
      const url = query
        ? `/articles/?search=${encodeURIComponent(query)}`
        : "/articles/";
      const response = await axios.get(url);
      setArticles(response.data.results || response.data);
      setIsLoading(false);
    } catch (error) {
      console.error("Error fetching articles:", error);
      setIsLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchArticles(searchQuery);
  };

  const handleViewAll = () => {
    setSearchQuery("");
    fetchArticles();
  };

  if (isLoading) {
    return (
      <div className="container">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  // Show only the 3 latest articles on home page
  const latestArticles = articles.slice(0, 3);

  return (
    <div className="container">
      <div style={{ textAlign: "center", marginBottom: "3rem" }}>
        <h1>🌟 Latest Articles</h1>
        <p
          style={{
            color: "var(--text-secondary)",
            fontSize: "1.1rem",
            marginBottom: "2rem",
          }}
        >
          Discover amazing stories and insights from our community
        </p>
      </div>

      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="🔍 Search articles..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit" className="btn">
          🔍 Search
        </button>
        <button
          type="button"
          onClick={handleViewAll}
          className="btn btn-secondary"
        >
          📋 View All
        </button>
      </form>

      <div style={{ display: "grid", gap: "2rem" }}>
        {latestArticles.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>

      {articles.length > 3 && (
        <div style={{ textAlign: "center", marginTop: "3rem" }}>
          <Link to="/articles" className="btn">
            📚 View All Articles
          </Link>
        </div>
      )}
    </div>
  );
}

// Articles Page Component
function ArticlesPage() {
  const [articles, setArticles] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async (query = "") => {
    try {
      const url = query
        ? `/articles/?search=${encodeURIComponent(query)}`
        : "/articles/";
      const response = await axios.get(url);
      setArticles(response.data.results || response.data);
      setIsLoading(false);
    } catch (error) {
      console.error("Error fetching articles:", error);
      setIsLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchArticles(searchQuery);
  };

  if (isLoading) {
    return (
      <div className="container">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{ textAlign: "center", marginBottom: "3rem" }}>
        <h1>📚 All Articles</h1>
        <p
          style={{
            color: "var(--text-secondary)",
            fontSize: "1.1rem",
            marginBottom: "2rem",
          }}
        >
          Explore our complete collection of articles
        </p>
      </div>

      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="🔍 Search articles..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit" className="btn">
          🔍 Search
        </button>
        <button
          type="button"
          onClick={() => fetchArticles()}
          className="btn btn-secondary"
        >
          🗑️ Clear
        </button>
      </form>

      <div style={{ display: "grid", gap: "2rem" }}>
        {articles.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>
    </div>
  );
}

// Article Card Component
function ArticleCard({ article }) {
  return (
    <div className="article-card">
      <h2>
        <Link to={`/articles/${article.id}`}>{article.title}</Link>
      </h2>
      <div className="article-meta">
        By {article.author?.user?.username || "Unknown"} •{" "}
        {new Date(article.created_at).toLocaleDateString()}
      </div>
      <p>{article.text.substring(0, 200)}...</p>
      {article.tags &&
        Array.isArray(article.tags) &&
        article.tags.length > 0 && (
          <div className="article-tags">
            {article.tags.map((tag, index) => (
              <span key={tag.id || `tag-${index}`} className="tag">
                {tag.name}
              </span>
            ))}
          </div>
        )}
    </div>
  );
}

// Article Detail Component
function ArticleDetail() {
  const { id: articleId } = useParams();
  const [article, setArticle] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    fetchArticle();
    fetchComments();
  }, [articleId]);

  const fetchArticle = async () => {
    try {
      const response = await axios.get(`/articles/${articleId}/`);
      setArticle(response.data);
      setIsLoading(false);
    } catch (error) {
      console.error("Error fetching article:", error);
      setIsLoading(false);
    }
  };

  const fetchComments = async () => {
    try {
      const response = await axios.get(`/articles/${articleId}/comments/`);
      setComments(response.data.results || response.data);
    } catch (error) {
      console.error("Error fetching comments:", error);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!user) {
      alert("Please login to add comments");
      return;
    }

    try {
      console.log("Adding comment with token:", localStorage.getItem("token"));
      console.log("Axios headers:", axios.defaults.headers.common);

      const response = await axios.post(`/articles/${articleId}/comments/`, {
        text: newComment,
      });
      console.log("Comment added successfully:", response.data);
      setNewComment("");
      fetchComments();
    } catch (error) {
      console.error("Error adding comment:", error);
      console.error("Error response:", error.response?.data);
      alert(
        `Error adding comment: ${error.response?.data?.error || error.message}`
      );
    }
  };

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm("Are you sure you want to delete this comment?")) {
      return;
    }

    try {
      await axios.delete(`/comments/${commentId}/`);
      fetchComments();
    } catch (error) {
      console.error("Error deleting comment:", error);
      alert("Error deleting comment");
    }
  };

  if (isLoading) {
    return (
      <div className="container">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  if (!article) {
    return <div className="container">Article not found</div>;
  }

  return (
    <div className="container">
      <article className="article-card" style={{ marginBottom: "3rem" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>
          {article.title}
        </h1>
        <div
          className="article-meta"
          style={{ fontSize: "1rem", marginBottom: "1.5rem" }}
        >
          By {article.author?.user?.username || "Unknown"} •{" "}
          {new Date(article.created_at).toLocaleDateString()}
        </div>
        {article.tags && article.tags.length > 0 && (
          <div className="article-tags" style={{ marginBottom: "2rem" }}>
            {article.tags &&
              Array.isArray(article.tags) &&
              article.tags.map((tag, index) => (
                <span key={tag.id || `tag-${index}`} className="tag">
                  {tag.name}
                </span>
              ))}
          </div>
        )}
        <div
          style={{
            marginTop: "2rem",
            whiteSpace: "pre-wrap",
            fontSize: "1.1rem",
            lineHeight: "1.8",
            color: "var(--text-primary)",
          }}
        >
          {article.text}
        </div>
      </article>

      <section
        style={{
          background: "var(--bg-primary)",
          padding: "2rem",
          borderRadius: "var(--radius-xl)",
          boxShadow: "var(--shadow-lg)",
          marginTop: "2rem",
        }}
      >
        <h3
          style={{
            marginBottom: "2rem",
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
          }}
        >
          💬 Comments ({comments.length})
        </h3>

        {user && (
          <form
            onSubmit={handleAddComment}
            style={{
              marginBottom: "2rem",
              background: "var(--bg-secondary)",
              padding: "1.5rem",
              borderRadius: "var(--radius-lg)",
            }}
          >
            <div className="form-group">
              <label htmlFor="comment">Add a comment:</label>
              <textarea
                id="comment"
                placeholder="Share your thoughts on this article..."
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                required
                rows="4"
              />
            </div>
            <button type="submit" className="btn">
              💬 Add Comment
            </button>
          </form>
        )}

        {comments.length === 0 ? (
          <div
            style={{
              textAlign: "center",
              color: "var(--text-muted)",
              padding: "2rem",
              fontStyle: "italic",
            }}
          >
            No comments yet. Be the first to share your thoughts!
          </div>
        ) : (
          <div style={{ display: "grid", gap: "1rem" }}>
            {comments.map((comment) => (
              <div key={comment.id} className="comment">
                <div className="comment-meta">
                  By {comment.author?.user?.username || "Unknown"} •{" "}
                  {new Date(comment.created_at).toLocaleDateString()}
                </div>
                <p>{comment.text}</p>
                {user && user.username === comment.author?.user?.username && (
                  <button
                    onClick={() => handleDeleteComment(comment.id)}
                    className="btn btn-danger"
                    style={{ marginTop: "0.5rem" }}
                  >
                    🗑️ Delete
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

// Login Component
function LoginPage() {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const result = await login(formData.username, formData.password);
    if (result.success) {
      navigate("/");
    } else {
      setError(result.error);
    }
  };

  return (
    <div className="container">
      <div style={{ maxWidth: "500px", margin: "0 auto", padding: "2rem 0" }}>
        <div style={{ textAlign: "center", marginBottom: "2rem" }}>
          <h1>🔑 Login</h1>
          <p style={{ color: "var(--text-secondary)", fontSize: "1.1rem" }}>
            Welcome back! Please sign in to your account
          </p>
        </div>

        {error && (
          <div className="error">
            {typeof error === "string" ? error : JSON.stringify(error)}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          style={{
            background: "var(--bg-primary)",
            padding: "2rem",
            borderRadius: "var(--radius-xl)",
            boxShadow: "var(--shadow-lg)",
          }}
        >
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              placeholder="Enter your username"
              value={formData.username}
              onChange={(e) =>
                setFormData({ ...formData, username: e.target.value })
              }
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={(e) =>
                setFormData({ ...formData, password: e.target.value })
              }
              required
            />
          </div>
          <button
            type="submit"
            className="btn"
            style={{ width: "100%", justifyContent: "center" }}
          >
            🔑 Login
          </button>
        </form>

        <p
          style={{
            marginTop: "2rem",
            textAlign: "center",
            color: "var(--text-secondary)",
          }}
        >
          Don't have an account?{" "}
          <Link
            to="/register"
            style={{ color: "var(--primary-color)", fontWeight: "600" }}
          >
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
}

// Register Component
function RegisterPage() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const result = await register(
      formData.username,
      formData.email,
      formData.password
    );
    if (result.success) {
      navigate("/");
    } else {
      setError(result.error);
    }
  };

  return (
    <div className="container">
      <div style={{ maxWidth: "500px", margin: "0 auto", padding: "2rem 0" }}>
        <div style={{ textAlign: "center", marginBottom: "2rem" }}>
          <h1>📝 Register</h1>
          <p style={{ color: "var(--text-secondary)", fontSize: "1.1rem" }}>
            Join our community and start sharing your stories
          </p>
        </div>

        {error && (
          <div className="error">
            {typeof error === "string" ? error : JSON.stringify(error)}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          style={{
            background: "var(--bg-primary)",
            padding: "2rem",
            borderRadius: "var(--radius-xl)",
            boxShadow: "var(--shadow-lg)",
          }}
        >
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              placeholder="Choose a unique username"
              value={formData.username}
              onChange={(e) =>
                setFormData({ ...formData, username: e.target.value })
              }
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              placeholder="Enter your email address"
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              placeholder="Create a strong password"
              value={formData.password}
              onChange={(e) =>
                setFormData({ ...formData, password: e.target.value })
              }
              required
            />
            <small>
              Password must contain at least 8 characters, including one
              uppercase letter, one lowercase letter, and one number.
            </small>
          </div>
          <button
            type="submit"
            className="btn"
            style={{ width: "100%", justifyContent: "center" }}
          >
            📝 Register
          </button>
        </form>

        <p
          style={{
            marginTop: "2rem",
            textAlign: "center",
            color: "var(--text-secondary)",
          }}
        >
          Already have an account?{" "}
          <Link
            to="/login"
            style={{ color: "var(--primary-color)", fontWeight: "600" }}
          >
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
}

// New Article Component
function NewArticlePage() {
  const [formData, setFormData] = useState({ title: "", text: "", tags: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const tags = formData.tags
        .split(",")
        .map((tag) => tag.trim())
        .filter((tag) => tag);
      console.log("Creating article with data:", {
        title: formData.title,
        text: formData.text,
        tags: tags,
      });

      const response = await axios.post("/articles/", {
        title: formData.title,
        text: formData.text,
        tags: tags,
      });
      setSuccess("Article created successfully!");
      setTimeout(() => {
        navigate(`/articles/${response.data.id}`);
      }, 1500);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          error.response?.data?.message ||
          "Error creating article"
      );
    }
  };

  return (
    <div className="container">
      <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem 0" }}>
        <div style={{ textAlign: "center", marginBottom: "2rem" }}>
          <h1>✍️ Create New Article</h1>
          <p style={{ color: "var(--text-secondary)", fontSize: "1.1rem" }}>
            Share your thoughts and ideas with the community
          </p>
        </div>

        {error && (
          <div className="error">
            {typeof error === "string" ? error : JSON.stringify(error)}
          </div>
        )}
        {success && (
          <div className="success">
            {typeof success === "string" ? success : JSON.stringify(success)}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          style={{
            background: "var(--bg-primary)",
            padding: "2rem",
            borderRadius: "var(--radius-xl)",
            boxShadow: "var(--shadow-lg)",
          }}
        >
          <div className="form-group">
            <label htmlFor="title">Title:</label>
            <input
              type="text"
              id="title"
              placeholder="Enter an engaging title for your article"
              value={formData.title}
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="text">Content:</label>
            <textarea
              id="text"
              placeholder="Write your article content here..."
              value={formData.text}
              onChange={(e) =>
                setFormData({ ...formData, text: e.target.value })
              }
              required
              rows="15"
            />
          </div>
          <div className="form-group">
            <label htmlFor="tags">Tags (comma-separated):</label>
            <input
              type="text"
              id="tags"
              value={formData.tags}
              onChange={(e) =>
                setFormData({ ...formData, tags: e.target.value })
              }
              placeholder="e.g., Django, Python, Tutorial, Web Development"
            />
            <small>
              Add relevant tags to help others discover your article
            </small>
          </div>
          <div
            style={{ display: "flex", gap: "1rem", justifyContent: "flex-end" }}
          >
            <Link to="/" className="btn btn-secondary">
              🚫 Cancel
            </Link>
            <button type="submit" className="btn">
              ✍️ Create Article
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Main App Component
function App() {
  const { isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="container">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <Router
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/articles" element={<ArticlesPage />} />
          <Route path="/articles/:id" element={<ArticleDetail />} />
          <Route path="/articles/new" element={<NewArticlePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </div>
    </Router>
  );
}

// App with Auth Provider
function AppWithAuth() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}

export default AppWithAuth;
