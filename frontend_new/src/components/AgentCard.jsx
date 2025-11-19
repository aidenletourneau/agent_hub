import { Button } from "@/components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function AgentCard({ agent }) {
  return (
    <Card className="w-100 max-w-sm">
      <CardHeader>
        <CardTitle>{agent.name}</CardTitle>
        <CardDescription>
          {agent.description}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <li>Url: {agent.url}</li>
        <li>Version: {agent.version}</li>
        <li>Protocol Version: {agent.protocalVersion}</li>
      </CardContent>
    </Card>
  )
}
