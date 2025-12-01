"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, Typography, Box, SwipeableDrawer} from "@mui/material";
import CoffeeIcon from "@mui/icons-material/LocalCafe";
import LocalCafeIcon from "@mui/icons-material/LocalCafe";

import { grey } from "@mui/material/colors";

function useDrowsinessStream() {
  const [score, setScore] = useState<any>(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        // expect { score: <number> } but don't transform it
        console.log("drowsiness message:", data.score);
        setScore(data.score);
      } catch (err) {
        console.error("failed to parse websocket message", err);
      }
    };

    ws.onerror = (err) => {
      console.error("websocket error", err);
    };

    return () => {
      ws.close();
    };
  }, []);

  return score; // e.g. { score: 0.73 }
}

// --- drawer constants (can move outside file)
const drawerBleeding = 56;

export default function Dashboard() {
  const drowsinessScore = useDrowsinessStream();
  const [drawerOpen, setDrawerOpen] = useState(false); 

  useEffect(() => {
    if (drowsinessScore == null) return; 
    if (drowsinessScore >= 0.3) {
      setDrawerOpen(true);
    } else {
      setDrawerOpen(false);
    }
  }, [drowsinessScore])


  const [speed, setSpeed] = useState(0);
  const maxSpeed = 140;
  const accelRate = 2;
  const decelRate = 2;
  const [keys, setKeys] = useState({ up: false, down: false });

  // --- Drowsiness score message ---- 

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowUp") setKeys((p) => ({ ...p, up: true }));
      if (e.key === "ArrowDown") setKeys((p) => ({ ...p, down: true }));
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.key === "ArrowUp") setKeys((p) => ({ ...p, up: false }));
      if (e.key === "ArrowDown") setKeys((p) => ({ ...p, down: false }));
    };

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setSpeed((prev) => {
        let next = prev;
        if (keys.up) next += accelRate;
        if (keys.down) next -= decelRate;
        next = Math.min(maxSpeed, Math.max(0, next));
        return next;
      });
    }, 16);
    return () => clearInterval(interval);
  }, [keys]);

  // helpers
  const mapRange = (
    v: number,
    inMin: number,
    inMax: number,
    outMin: number,
    outMax: number
  ) => outMin + ((v - inMin) * (outMax - outMin)) / (inMax - inMin);

  const toRad = (deg: number) => (deg * Math.PI) / 180;

  const centerX = 130;
  const centerY = 140;
  const radius = 95;
  const circumference = Math.PI * radius;

  const tachAngle = mapRange(speed, 0, maxSpeed, -180, 0);
  const needleLen = 80; // was 80
  const needleX = centerX + needleLen * Math.cos(toRad(tachAngle));
  const needleY = centerY + needleLen * Math.sin(toRad(tachAngle));

  const speedPercent = speed / maxSpeed;
  const arcDashoffset = circumference * (1 - speedPercent);

  return (
    <Box
      sx={{
        height: "100vh",
        backgroundColor: "#111",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Box sx={{ display: "flex", gap: 6, alignItems: "center" }}>
        {/* LEFT: Tachometer (no labels) */}
        <Card
          sx={{
            width: 280,
            height: 280,
            backgroundColor: "#111",
            color: "white",
            borderRadius: 3,
            boxShadow: "none",
            border: "2px solid #fff",
          }}
        >
          <CardContent
            sx={{
              textAlign: "center",
              width: "100%",
              padding: 0,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "flex-end",
              height: "100%",
            }}
          >
            <svg width="260" height="180" viewBox="0 0 260 180">
              <path
                d="M40,140 A110,110 0 0 1 220,140"
                stroke="#fff"
                strokeWidth="8"
                fill="none"
              />
              <path
                d="M55,140 A95,95 0 0 1 205,140"
                stroke="#555"
                strokeWidth="10"
                fill="none"
              />
              <path
                d="M75,140 A70,70 0 0 1 185,140"
                stroke="#fff"
                strokeWidth="3"
                fill="none"
              />
              <line
                x1={centerX}
                y1={centerY}
                x2={needleX}
                y2={needleY}
                stroke="#fff"
                strokeWidth="3"
              />
            </svg>
          </CardContent>
        </Card>

        {/* CENTER: number + miles + bar */}
        {!drawerOpen && (
        <Card
          sx={{
            width: 180,
            height: 180,
            backgroundColor: "#111",
            color: "white",
            borderRadius: 3,
            boxShadow: "none",
            border: "2px solid #fff",
            display: "flex",
          }}
        >
          <CardContent
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              width: "100%",
              gap: 1,
            }}
          >
            <Typography variant="h3" sx={{ fontWeight: "bold" }}>
              {Math.round(speed)}
            </Typography>
            <Box sx={{ width: "40px", height: "2px", bgcolor: "#fff", my: 0.5 }} />
            <Typography variant="body2" sx={{ letterSpacing: 1 }}>
              1234 miles
            </Typography>
            <Box
              sx={{
                display: "flex",
                gap: 0.3,
                mt: 1.5,
              }}
            >
              {Array.from({ length: 12 }).map((_, i) => (
                <Box
                  key={i}
                  sx={{
                    width: 8,
                    height: 14,
                    border: "1px solid #fff",
                    bgcolor: i < 3 ? "#ff3b3b" : "transparent",
                  }}
                />
              ))}
            </Box>
          </CardContent>
        </Card>
        )}

        {/* RIGHT: Speedometer (no labels, just arcs + big number) */}
        <Card
          sx={{
            width: 280,
            height: 280,
            backgroundColor: "#111",
            color: "white",
            borderRadius: 3,
            boxShadow: "none",
            border: "2px solid #fff",
          }}
        >
          <CardContent
            sx={{
              textAlign: "center",
              width: "100%",
              padding: 0,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "flex-end",
              height: "100%",
            }}
          >
            <svg width="260" height="180" viewBox="0 0 260 180">
              <path
                d="M40,135 A110,110 0 0 1 220,135"
                stroke="#444"
                strokeWidth="10"
                fill="none"
                strokeLinecap="round"
              />
              <path
                d="M55,135 A95,95 0 0 1 205,135"
                stroke="#777"
                strokeWidth="4"
                fill="none"
                strokeDasharray="2 4"
              />
              <path
                d="M55,135 A95,95 0 0 1 205,135"
                stroke="#fff"
                strokeWidth="4"
                fill="none"
                strokeDasharray={circumference}
                strokeDashoffset={arcDashoffset}
                style={{ transition: "stroke-dashoffset 0.1s linear" }}
              />
              <text
                x={centerX}
                y="155"
                fill="#fff"
                fontSize="40"
                textAnchor="middle"
                dominantBaseline="middle"
              >
                {Math.round(speed)}
              </text>
            </svg>
          </CardContent>
        </Card>
      </Box>

      {/* Bottom auto-opening drawer for drowsiness */}
      <SwipeableDrawer
        anchor="bottom"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        onOpen={() => setDrawerOpen(true)}
        swipeAreaWidth={56}
        disableSwipeToOpen
        keepMounted
        slotProps={{
          paper : {
            sx: {
              height: "40vh",
              overflow: "visible",
              backgroundColor: "#111",
              color: "#fff",
            },
          }
        }}
      >
        {/* Grip + coffee icon header */}
        <Box
          sx={{
            position: "absolute",
            top: -56,
            borderTopLeftRadius: 8,
            borderTopRightRadius: 8,
            right: 0,
            left: 0,
            backgroundColor: "#111",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            py: 1,
          }}
        >
          <Box
            sx={{
              width: 30,
              height: 6,
              backgroundColor: grey[700],
              borderRadius: 3,
              mb: 1,
            }}
          />
          <LocalCafeIcon sx={{ fontSize: 32 }} />
        </Box>

        {/* Drawer body */}
        <Box sx={{ px: 3, pb: 3, pt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Take a break
          </Typography>
          <Typography variant="body2">
            Your drowsiness score is {drowsinessScore?.toFixed(2)}.
          </Typography>
        </Box>
      </SwipeableDrawer>
    </Box>
  );
}
