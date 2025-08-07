# Database Setup Guide

This guide explains how to set up and use the database for the LendingVerse P2P lending platform.

## Prerequisites

- Node.js (v14 or higher)
- PostgreSQL (v12 or higher)
- Prisma CLI (`npm install -g prisma`)

## Setup Steps

### 1. Create a PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create a database
CREATE DATABASE lending_verse;

# Create a user (optional)
CREATE USER lending_user WITH ENCRYPTED PASSWORD 'your_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE lending_verse TO lending_user;

# Exit PostgreSQL
\q
```

### 2. Configure Environment Variables

Copy the `.env.example` file to `.env` and update the database connection string:

```
DATABASE_URL="postgresql://lending_user:your_password@localhost:5432/lending_verse?schema=public"
```

### 3. Generate Prisma Client

```bash
# Install dependencies
npm install

# Generate Prisma client
npx prisma generate
```

### 4. Run Migrations

```bash
# Create a migration
npx prisma migrate dev --name init

# Apply the migration
npx prisma migrate deploy
```

### 5. Seed the Database (Optional)

Create a seed script in `prisma/seed.ts`:

```typescript
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

async function main() {
  // Create admin user
  const admin = await prisma.user.create({
    data: {
      email: 'admin@lendingverse.com',
      passwordHash: 'hashed_password', // Use proper hashing in production
      role: 'ADMIN',
      profile: {
        create: {
          firstName: 'Admin',
          lastName: 'User',
        },
      },
    },
  });

  console.log('Database seeded successfully');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

Run the seed script:

```bash
npx prisma db seed
```

## Database Management

### Prisma Studio

Prisma provides a GUI to view and edit your data:

```bash
npx prisma studio
```

This will open a web interface at http://localhost:5555.

### Migrations

When you make changes to the schema:

```bash
# Create a migration
npx prisma migrate dev --name your_migration_name

# Apply to production
npx prisma migrate deploy
```

### Reset Database

To reset your database during development:

```bash
npx prisma migrate reset
```

This will drop all tables, recreate them, and run the seed script.

## Using the Database in Code

Import the Prisma client in your services:

```typescript
import prisma from '../config/database';

export class UserService {
  async findUserByEmail(email: string) {
    return prisma.user.findUnique({
      where: { email },
      include: { profile: true },
    });
  }
  
  async createUser(userData) {
    return prisma.user.create({
      data: userData,
    });
  }
}
```

## Transactions

For operations that require multiple database changes:

```typescript
import prisma from '../config/database';

export class LoanService {
  async createLoanMatch(loanRequestId: string, loanOfferId: string) {
    return prisma.$transaction(async (tx) => {
      // Create the match
      const match = await tx.loanMatch.create({
        data: {
          loanRequestId,
          loanOfferId,
          matchScore: 85, // Calculate this based on criteria
          status: 'PENDING',
        },
      });
      
      // Update the loan request status
      await tx.loanRequest.update({
        where: { id: loanRequestId },
        data: { status: 'PENDING' },
      });
      
      // Update the loan offer status
      await tx.loanOffer.update({
        where: { id: loanOfferId },
        data: { status: 'MATCHED' },
      });
      
      return match;
    });
  }
}
```

## Performance Considerations

- Use appropriate indexes for frequently queried fields
- Use pagination for large result sets
- Use transactions for operations that require consistency
- Consider using database connection pooling in production

## Backup and Recovery

Regularly back up your PostgreSQL database:

```bash
pg_dump -U lending_user -d lending_verse > backup.sql
```

To restore from a backup:

```bash
psql -U lending_user -d lending_verse < backup.sql
```