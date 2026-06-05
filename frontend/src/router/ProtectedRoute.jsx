export default function ProtectedRoute({ children }) {
  const authenticated = true;
  return authenticated ? children : <div>Access Denied</div>;
}
