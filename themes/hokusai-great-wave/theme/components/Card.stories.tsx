import type { Meta, StoryObj } from '@storybook/react';
import Card from './Card';

const meta  : Meta<typeof Card> = {
  title: 'Components/Card',
  component: Card,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Card>;

export const Elevated: Story = { args={{ variant: 'elevated', children: 'Card content' }} };
export const Filled: Story = { args={{ variant: 'filled', children: 'Card content' }} };
export const Outlined: Story = { args={{ variant: 'outlined', children: 'Card content' }} };
